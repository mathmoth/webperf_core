# -*- coding: utf-8 -*-
# pylint: disable=too-many-lines
import base64
import re
import urllib
import urllib.parse
from helpers.hash_helper import create_sha256_hash
from helpers.setting_helper import get_config
from models import Rating

# pylint: disable=too-many-arguments
def rate_csp(result_dict, global_translation, local_translation,
             org_domain, org_www_domain, domain, should_create_recommendation):
    """
    This function rates the Content Security Policy (CSP) of a given domain.

    Parameters:
    result_dict (dict): A dictionary containing the results of the CSP checks.
    global_translation (function): A function to translate text to a global language.
    local_translation (function): A function to translate text to a local language.
    org_domain (str): The original domain.
    org_www_domain (str): The original domain with 'www.' prefix.
    domain (str): The domain to be rated.
    should_create_recommendation (bool): A flag indicating whether to create a recommendation.

    Returns:
    Rating: A Rating object containing the overall rating,
            standards rating, and integrity and security rating.
    """
    rating = Rating(global_translation, get_config('general.review.improve-only'))
    if not isinstance(result_dict[domain], dict):
        return rating

    if domain not in (org_domain, org_www_domain):
        return rating

    if 'CSP-HEADER-FOUND' in result_dict[domain]['features'] or\
            'CSP-META-FOUND' in result_dict[domain]['features']:
        total_number_of_sitespeedruns = result_dict['visits']

        if 'CSP-UNSUPPORTED-IN-META' in result_dict[domain]['features']:
            sub_rating = Rating(
                global_translation,
                get_config('general.review.improve-only'))
            sub_rating.set_overall(1.0)
            sub_rating.set_standards(1.0,
                                     local_translation(
                                         'TEXT_REVIEW_CSP_UNSUPPORTED_IN_META'
                                         ).format(domain))
            rating += sub_rating

        rating += rate_csp_depricated(domain, result_dict, local_translation, global_translation)

        for policy_name in CSP_POLICIES_SUPPORTED_SRC:
            policy_object = None
            if policy_name in result_dict[domain]['csp-objects']:
                policy_object = result_dict[domain]['csp-objects'][policy_name]
            else:
                continue

            rating += rate_csp_policy(
                domain,
                total_number_of_sitespeedruns,
                policy_object,
                local_translation,
                global_translation)

        rating += rate_csp_fallbacks(domain, result_dict, local_translation, global_translation)

    elif 'HTML-FOUND' in result_dict[domain]['features'] and\
            (domain in (org_domain, org_www_domain)):
        rating = Rating(global_translation, get_config('general.review.improve-only'))
        rating.set_overall(1.0)
        rating.set_standards(1.0,
            local_translation('TEXT_REVIEW_CSP_NOT_FOUND').format(domain))
        rating.set_integrity_and_security(1.0,
            local_translation('TEXT_REVIEW_CSP_NOT_FOUND').format(domain))

    final_rating = create_final_csp_rating(global_translation, local_translation, domain, rating)

    if should_create_recommendation and 'csp-findings' in result_dict[domain]:
        rec_rating, text_recommendation = create_csp_recommendation(
            domain,
            result_dict,
            org_domain,
            org_www_domain,
            local_translation,
            global_translation)
        if rec_rating.get_integrity_and_security() > final_rating.get_integrity_and_security():
            final_rating.overall_review = text_recommendation + final_rating.overall_review

    return final_rating

def append_sri_data(req_url, req_domain, res, org_domain, result):
    """
    Appends Subresource Integrity (SRI) data for various types of content.

    This function checks the type of content (HTML) and
    calls the appropriate function to append the SRI data to the result dictionary. 

    Args:
        req_url (str): The requested URL.
        req_domain (str): The requested domain.
        res (dict): The response dictionary containing the content.
        org_domain (str): The original domain.
        result (dict): The result dictionary where the CSP data will be appended.

    Returns:
        bool: True if there is a match in the CSP findings, False otherwise.
    """
    csp_findings_match = False
    if 'content' in res and 'text' in res['content']:
        if 'mimeType' in res['content'] and 'text/html' in res['content']['mimeType']:
            csp_findings_match = csp_findings_match or append_sri_data_for_html(
                req_url,
                req_domain,
                res,
                org_domain,
                result)

def append_sri_data_for_html(req_url, req_domain, res, org_domain, result):
    """
    Appends Subresource Integrity (SRI) data for HTML content and linked resources.

    This function parses the HTML content and identifies the SRI from attributes.
    It also identifies linked resources such as style, and script.
    It then appends the SRI data for these resources to the result dictionary.

    Args:
        req_url (str): The requested URL.
        req_domain (str): The requested domain.
        res (dict): The response dictionary containing the HTML content.
        org_domain (str): The original domain.
        result (dict): The result dictionary where the SRI data will be appended.

    Returns:
        bool: True if there is a match in the CSP findings, False otherwise.
    """
    csp_findings_match = False
    # Reference: https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity
    # https://www.srihash.org/
    content = res['content']['text']
    regex = (
                        r'(?P<raw>(?P<name>link|script)<.*? integrity="(?P<integrity>[^"]+)".*?>)'
                    )
    matches = re.finditer(regex, content, re.MULTILINE)
    for _, match in enumerate(matches, start=1):
        raw = match.group('raw')
        name = match.group('name').lower()
        integrity = match.group('integrity')

        # link elements with attributes:
        # - rel="stylesheet"
        # - rel="preload"
        # - rel="modulepreload"

    csp_findings_match = csp_findings_match or append_csp_data_for_linked_resources(
        req_domain,
        org_domain,
        result,
        content)

    regex = r'<(?P<type>style|script|form)>'
    matches = re.finditer(regex, content, re.DOTALL | re.IGNORECASE | re.MULTILINE)
    for _, match in enumerate(matches, start=1):
        element_name = match.group('type').lower()
        if element_name in ('style', 'script'):
            key = f'\'unsafe-inline\'|{element_name}'
            if key not in result[org_domain]['csp-findings']['quotes']:
                result[org_domain]['csp-findings']['quotes'].append(key)
            csp_findings_match = True
        elif element_name == 'form':
            element_url = url_2_host_source(req_url, req_domain)
            o = urllib.parse.urlparse(element_url)
            element_domain = o.hostname
            if element_domain == org_domain:
                key = f'\'self\'|{element_name}'
                if key not in result[org_domain]['csp-findings']['quotes']:
                    result[org_domain]['csp-findings']['quotes'].append(key)
                csp_findings_match = True
            else:
                key = f'{element_domain}|{element_name}'
                if key not in result[org_domain]['csp-findings']['host-sources']:
                    result[org_domain]['csp-findings']['host-sources'].append(key)
                csp_findings_match = True
    return csp_findings_match

def append_csp_data_for_linked_resources(req_domain, org_domain, result, content):
    """
    Appends Content Security Policy (CSP) data for linked resources in a given HTML content.

    This function parses the HTML content and identifies linked resources such as
    style, link, script, img, iframe, form, base, and frame elements. 
    It then appends the CSP data for these resources to the result dictionary.

    Args:
        req_domain (str): The requested domain.
        org_domain (str): The original domain.
        result (dict): The result dictionary where the CSP data will be appended.
        content (str): The HTML content to be parsed.

    Returns:
        bool: True if there is a match in the CSP findings, False otherwise.
    """
    csp_findings_match = False
    regex = (
                    r'(?P<raw><(?P<type>style|link|script|img|iframe|form|base|frame)[^>]'
                    r'*((?P<attribute>src|nonce|action|href)="(?P<value>[^"]+)"[^>]*>))'
                )

    matches = re.finditer(regex, content, re.MULTILINE)
    for _, match in enumerate(matches, start=1):
        element_name = match.group('type').lower()
        attribute_name = match.group('attribute').lower()
        attribute_value = match.group('value').lower()

        element_url = url_2_host_source(attribute_value, req_domain)
        o = urllib.parse.urlparse(element_url)
        element_domain = o.hostname
        if element_domain is None and element_url.startswith('data:'):
            element_domain = 'data:'
        elif element_domain == org_domain:
            element_domain = '\'self\''

        if attribute_name == 'nonce':
            key = f'\'nonce-<your-nonce>\'|{element_name}'
            if key not in result[org_domain]['csp-findings']['quotes']:
                result[org_domain]['csp-findings']['quotes'].append(key)
            csp_findings_match = True
        elif attribute_name == 'src':
            if element_domain is not None:
                key = f'{element_domain}|{element_name}'
                if key not in result[org_domain]['csp-findings']['host-sources']:
                    result[org_domain]['csp-findings']['host-sources'].append(key)
                csp_findings_match = True
        elif attribute_name == 'action' and element_name == 'form':
            key = f'{element_domain}|form-action'
            if key not in result[org_domain]['csp-findings']['host-sources']:
                result[org_domain]['csp-findings']['host-sources'].append(key)
            csp_findings_match = True
    return csp_findings_match

def url_2_host_source(url, domain):
    """
    Converts a given URL to a secure (https) URL if it's not already.

    Args:
        url (str): The URL to be converted.
        domain (str): The domain to be used if the URL doesn't contain a domain.

    Returns:
        str: The converted secure URL.
    """
    if url.startswith('//'):
        return url.replace('//', 'https://')
    if 'https://' in url:
        return url
    if '://' in url:
        return url
    if ':' in url:
        return url
    return f'https://{domain}/{url}'
