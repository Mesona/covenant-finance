# covenant-finance
A program for the purpose of yearly advancement and tracking of covenant finances and advancement.

Webpage Navigation Chat:
https://lucid.app/lucidchart/2f313fc1-cce1-4b49-97aa-bbb3888e4326/edit?invitationId=inv_9190d9ef-9b74-41b4-82db-e20480a2a77f

TODO:
  * Example usage
  * Add "Advance year" function
  * Front end tests
  * Cap number of covenants a user can have
  * User registration email validation
  * Cap number of income sources a covenant can have
  * Add tooltip to explain 250 income for greater virtue, 100 income for typical
  * Income source value modifiers tied to inflation enabled/disabled
  * Add crafter/specialst options for people who do things not directly related to cost savings
  * Add tooltips to describe different roles under covenfolk (Specialist vs Crafter for example)
  * Add column in covenfolk to show max savings possible per crafter/specialist
  * Button to automatically calculate number of servants and teamsters required

BUGS TO FIX:
  * Login with non existant user throws error
  * Fail covenant validation throws error page
  * Fail lab validation (unique name) throws error page
  * Covenant names are currently globally unique, need to be unique per user
  * User's covenants do not populate until new login (create covenant redirect missing data)
  * New Covenent screen's Income Sources +/- button is offset on the first entry for some reason (create multiple and look at the first)
  * Specialsts do not provide savings
