��    .      �              �     �               4     I     Z     k     �     �     �     �  #   �     �          /     J  #   `     �     �     �     �     �            (   4     ]     {  +   �  +   �  0   �  9   $  /   ^     �     �     �  (   �  #     "   9  (   \  "   �  "   �  *   �     �          &  J  :  _  �	  *   �            
   '     2  3   @     t     �  
   �     �     �     �               (  !   C     e     �     �     �     �  /   �  *      +   +     W     m     �  $   �  +   �  %   �  .        D     [     s     �      �     �     �  '   �  )   &  0   P  (   �  *   �     �   TEXT_COMMAND_USAGE TEXT_EXCEPTION TEXT_REQUEST_UNKNOWN TEXT_REQUEST_WEBPAGE TEXT_SITE_RATING TEXT_SITE_REVIEW TEXT_SITE_UNAVAILABLE TEXT_TESTING_NUMBER_OF_SITES TEXT_TESTING_SITE TEXT_TEST_END TEXT_TEST_RATING_ALLY TEXT_TEST_RATING_INTEGRITY_SECURITY TEXT_TEST_RATING_OVERVIEW TEXT_TEST_RATING_PERFORMANCE TEXT_TEST_RATING_STANDARDS TEXT_TEST_REVIEW_ALLY TEXT_TEST_REVIEW_INTEGRITY_SECURITY TEXT_TEST_REVIEW_OVERVIEW TEXT_TEST_REVIEW_PERFORMANCE TEXT_TEST_REVIEW_RATING_ITEM TEXT_TEST_REVIEW_STANDARDS TEXT_TEST_START TEXT_TEST_START_HEADER TEXT_TEST_VALID_ARGUMENTS TEXT_TEST_VALID_ARGUMENTS_A11Y_STATEMENT TEXT_TEST_VALID_ARGUMENTS_CSS TEXT_TEST_VALID_ARGUMENTS_EMAIL TEXT_TEST_VALID_ARGUMENTS_ENERGY_EFFICIENCY TEXT_TEST_VALID_ARGUMENTS_GOOGLE_LIGHTHOUSE TEXT_TEST_VALID_ARGUMENTS_GOOGLE_LIGHTHOUSE_A11Y TEXT_TEST_VALID_ARGUMENTS_GOOGLE_LIGHTHOUSE_BEST_PRACTICE TEXT_TEST_VALID_ARGUMENTS_GOOGLE_LIGHTHOUSE_SEO TEXT_TEST_VALID_ARGUMENTS_HTML TEXT_TEST_VALID_ARGUMENTS_HTTP TEXT_TEST_VALID_ARGUMENTS_PA11Y TEXT_TEST_VALID_ARGUMENTS_PAGE_NOT_FOUND TEXT_TEST_VALID_ARGUMENTS_SITESPEED TEXT_TEST_VALID_ARGUMENTS_SOFTWARE TEXT_TEST_VALID_ARGUMENTS_STANDARD_FILES TEXT_TEST_VALID_ARGUMENTS_TRACKING TEXT_TEST_VALID_ARGUMENTS_WEBBKOLL TEXT_TEST_VALID_ARGUMENTS_YELLOW_LAB_TOOLS TEXT_WEBSITE_URL_ADDED TEXT_WEBSITE_URL_DELETED TEXT_WEBSITE_X_OF_Y Project-Id-Version: PACKAGE VERSION
POT-Creation-Date: 2020-05-23 17:29+0200
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: cockroacher <cockroacher@noyb.eu>
Language-Team: Swedish <team@webperf.se>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Generated-By: pygettext.py 1.5
 
	WebPerf Core

	Använd så här:
default.py -u https://webperf.se

	Val och argument:
	-h/--help			: Hjälp och hur du använder skriptet
	-u/--url <site url>		: webbplatsens adress att testa
	-t/--test <test nummer>		: kör ett specifikt test (ange ? för att lista tillgängliga tester)
	-r/--review			: visar omdömen direkt i terminalen
	-i/--input <file path>		: sökväg för input-fil (.json/.sqlite)
	-i/--input-skip <nummer>	: antal att hoppa över
	-i/--input-take <nummer>	: antal att testa
	-o/--output <file path>		: sökväg till output-fil (.json/.csv/.sql/.sqlite/.md)
	-A/--addUrl <site url>		: webbplatsens adress/url (ett krav när du använder -i/--input)
	-D/--deleteUrl <site url>	: webbplats adress/url (ett krav när du använder -i/--input)
	-L/--language <lang code>	: språk som används för output(en = default/sv)
	--setting <nyckel>=<värde>	: Använd inställning för nuvarande körning
					  (ange ? för att lista tillgängliga inställningar)
	--save-setting <filnamn>	: Skapa egen inställningsfil från nuvarande använda inställningar
					  (Du bör använda 'settings.json') Fel, någon behöver ta en titt på detta. #{0}:  #{0}: Webbsida  ### Betyg: ### Omdöme:
 Fel, det gick inte att läsa in den begärda sidan. Webbadresser som testas {0} # Testar adress {0} Klar: {0}
 - Tillgänglighet: {0}
 - Integritet & säkerhet: {0}
 
- Övergripande: {0}
 - Prestanda: {0}
 - Standarder: {0}
 #### Tillgänglighet:
{0} #### Integritet & säkerhet:
{0} 
#### Övergripande:
{0} #### Prestanda:
{0} {0} ( {1:.2f} betyg )
 #### Standarder:
{0} Startad: {0} ############################################### Giltiga argument att välja på -t/--test: -t 26	: Tillgänglighetsredogörelse (Alfa) -t 7	: CSS-validering -t 24	: E-post (Beta) -t 22	: Energieffektivitet -t 1	: Prestanda (Google Lighthouse) -t 10	: Tillgänglighet (Google Lighthouse) -t 5	: God praxis (Google Lighthouse) -t 4	: Sökmotoroptimering (Google Lighthouse) -t 6	: HTML-validering -t 21	: HTTP & nätverk -t 18	: Tillgänglighet (Pa11y) -t 2	: 404 (sida finns inte) -t 15	: Prestanda (Sitespeed.io) -t 25	: Mjukvara (Alfa) -t 9	: Standardfiler -t 23	: Spårning och integritet (Beta) -t 20	: Integritet & säkerhet (Webbkoll) -t 17	: Kvalitet på frontend (Yellow Lab Tools) Webbplats med adress: {0} har lats till
 Webbplats med adress: {0} har tagits bort
 Webbplats {0} av {1}.
 