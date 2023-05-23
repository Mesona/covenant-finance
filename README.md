# covenant-finance
A program for the purpose of yearly advancement and tracking of covenant finances and advancement.

Webpage Navigation Chart:
https://lucid.app/lucidchart/2f313fc1-cce1-4b49-97aa-bbb3888e4326/edit?invitationId=inv_9190d9ef-9b74-41b4-82db-e20480a2a77f

TODO BEFORE ALPHA:
  * Example usage
  * Front end tests
  * Fix back end tests, too
  * Add tests for charged items
  * Cap number of covenants a user can have
  * Cap number of income sources a covenant can have
  * Income source value modifiers tied to inflation enabled/disabled
  * Add crafter/specialst options for people who do things not directly related to cost savings
  * Add column in covenfolk to show max savings possible per crafter/specialist
  * Button to automatically calculate number of servants and teamsters required
  * Limit database usage to prevent excess costs (might not be a problem in a free tier ec2 host?)

TODO BEFORE BETA:
  * User registration email validation
  * User change password
  * Password recovery
  * Add tooltip to explain 250 income for greater virtue, 100 income for typical
  * Add tooltips to describe different roles under covenfolk (Specialist vs Crafter for example)
  * Add tooltips in general
  * Replace error screens with proper errors
  * Export covenant
  * Cost breakdown by type in covenant page

TODO BEFORE RELEASE:
  * Graphics
  * Basic security audit (Cross site forgery, DDOS, etc)
  * Throttle on failed logins
  * Database backup (1 week? 3 weeks?)

BUGS TO FIX:
  * Login with non existant user throws error
  * Fail covenant validation throws error page
  * Fail lab validation (unique name) throws error page
  * Covenant names are currently globally unique, need to be unique per user
  * User's covenants do not populate until new login (create covenant redirect missing data)
  * New Covenent screen's Income Sources +/- button is offset on the first entry for some reason (create multiple and look at the first)
  * Specialsts do not provide savings
