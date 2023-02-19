# Flat Finder app Requirements

|ID|Requirement|Type|Priority|Use Case|
|--|-----------|----|--------|--------|
|1 |Each user must be identified with their corporate email address|Functional (D)|Core|-|
|2 |The system must have two types of users: consultant and system administrator.|Functional|Core|-|
|3 |Only admins should be able to access the admin portal|Functional|Core|-|
|4 |The system should periodically fetch listings from external APIs and update the listings cached in the system|Functional|Optional|-|
|5 |The application's interface must have multi-language support based on different regions with FDM centres|Functional|Core|-|
|6 |Users will log in using Single Sign On (SSO) with their corporate accounts|Functional|Core|Login|
|7 |Users will be registered in the system the first time they log in using Single Sign On|Functional|Core|Login|
|8 |Upon first logging into the system, consultants should be prompted to complete their profile (Work site, Slack member ID, optional photo)|Functional (D)|Core|Complete Profile|
|9 |Profiles can be completed later, but no listing may be posted without a complete profile|Functional|Core|Complete Profile|
|10|Users must be able to logout|Functional|Core|Logout|
|11|Admins should be able to view users registered in the system|Functional|Core|View users
|12|Admins should be able to make other users admins, either by selecting from the list of users or by manually entering their corporate email address|Functional|Core|Make user admin|
|13|Admins should be able to remove users from the system|Functional|Optional|Remove User|
|14|Removing a user should delete all of their user data and listings, but preserve the contents of their reviews|Functional (D)|Optional|Remove User|
|15|By default all external sources should be enabled|Functional|Core|Configure external sources|
|16|Admins should be able to enable external sources for pulling listings|Functional|Optional|Configure external sources|
|17|Admins should be able to disable external sources for pulling listings|Functional|Optional|Configure external sources|
|18|Disabling an external source should hide all listings from that source and pause the automatic pulling of listings from that source|Functional|Optional|Configure external sources|
|19|Users should be able to view all non-hidden listings in the system|Functional|Core|View Listings|
|21|Listings should be paginated|Functional|Core|View Listings|
|22|Each accommodation listing in the list must have a title, photo, brief description, rating, source, price, distance from the specified location, postal code, accommodation type, and "favourite" indicator|Functional (D)|Core|View Accommodation Listings|
|23|Each seeking listing in the list must have a title, brief description, distance from the specified location, and "favourite" indicator|Functional (D)|Core|View Seeking Listings|
|24|Seeking listings should be sorted by distance from specified location|Functional|Core|View Seeking Listings|
|25|Admins should be able to remove any listings from the system|Functional|Core|Remove Listing|
|26|Users should be prompted to specify the location they wish to search near, and select a maximum distance from this location|Functional|Core|Filter Listings|
|26a|Admins should be able to filter listings by "FDM" to view all internal listings in order to bypass specifying the location|Functional|Optional|Filter Listings|
|28|Users should have the option of filtering accommodation listings by source (internal/external/both)|Functional|Optional|Filter Accommodation Listings|
|29|Users should have the option of filtering accommodation listings by maximum price|Functional|Optional|Filter Accommodation Listings|
|30|Users should be able to sort accommodation listings by price|Functional|Core|Sort Accommodation Listings|
|31|Users should be able to sort accommodation listings by distance from the specified location|Functional|Core|Sort Accommodation Listings|
|32|Users should be able to enter a detailed view of a selected listing from the search results|Functional|Core|View Listing Details|
|33|The detailed listing view should have a Google Maps integration with the location of the listing|Functional|Core|View Listing Details|
|34|The detailed accommodation listing view must have a title, full description, gallery of photos, living condition information (e.g. pets, smoking, number of tenants) rating, source, price breakdown, full address, number of rooms, a list of amenities, contact information, link to the original external listing (if applicable), and a list of reviews for the property and listing author|Functional (D)|Core|View Accommodation Listing Details|
|35|The detailed seeking accommodation listing view must have a title, full description, contact information and preferred location|Functional (D)|Core|View Seeking Listing Details|
|36|Users should be able to return from a detailed listing view to where they were in the search results|Functional|Core|View Listings|
|37|Users should be able to compare the features of two accommodation listings feature (e.g. price, location, conditions etc.)|Functional|Optional|Compare Accommodation Listings|
|38|Consultants should have the option of adding a listing to their favourites|Functional|Optional|Add Listing to Favourites|
|38a|If an external listing is favourited by at least 1 consultant, it is cached in the system|Functional|Optional|Add Listing to Favourites|
|39|Consultants should have the option of viewing their favourited listings|Functional|Optional|View Favourite Listings|
|40|Consultants should have the option of removing a listing from their favourites|Functional|Optional|Remove Listing from Favourites|
|40a|If an external listing is no longer favourited by any consultant, it is removed from the system cache|Functional|Optional|Remove Listing from Favourites|
|41|Consultants should be able to leave a textual review along with a rating (0-5) on any accommodation listing|Functional|Optional|Leave Review|
|42|Consultants should be able to leave a textual review along with a rating (0-5) on any listing author|Functional|Optional|Leave Review|
|43|Consultants should be able to create listings about an accommodation, providing all the details specified in RQ34|Functional|Core|Create Accommodation Listing|
|44|When creating an accommodation listing, consultants should be able to upload 0-15 photos|Functional (D)|Core|Create Accommodation Listing
|45|Consultants should be able to create listings about seeking accommodation, providing all the details specified in RQ35|Functional|Core|Create Seeking Listing|
|46|Consultants should be able to view a list of listings they have created|Functional|Core|View own Listings|
|47|Consultants should be able to edit the listings they have created|Functional|Core|Edit Listing|
|48|Consultants should be able to remove the listings they have created|Functional|Core|Remove Listing|
|49|Admins should be able to remove any listing|Functional|Core|Remove Listing|
|50|Consultants should be able to view the profiles of other consultants that have posted a listing|Functional|Core|View Profile|
|51|Consultant profiles should show their name, optionally a photo, the site they currently work at and links to their corporate chat (Slack/Teams) and a list of reviews left by other consultants|Functional (D)|Core|View Profile|
|52|Admins should be able to enable/disable corporate chat integrations (Slack/Teams)|Functional|Optional|Administrate Chat Integrations|
|53|The system must not allow performing any activities without authentication|Functional|Core|-|
|55|The application should comply with the Web Content Accessibility Guidelines (WCAG) 2.1 level AA|Non-functional Accessibility|Core|-|
|56|The application must support all major web browsers: Google Chrome, Mozilla Firefox, Microsoft Edge and Safari|Non-functional Compatibility|Core|-|
|57|The application should have a responsive web design, allowing it to adjust its visuals based on the screen size, supporting resolutions from 320x240px with no upper bound|Non-functional Usability|Core|-|
|58|The system must be able to support 1000-1500 simultaneous users|Non-functional Scalability|Core|-|
|59|Each photo uploaded by a user must have a maximum file size of 5MB|Non-functional Resource constraints|Core|-|
|60|The database should be backed up once a day|Non-functional Backup|Core|-|
|61|The system must have an administrator's manual specifying how to use the admin features|Non-functional Documentation|Core|-|
|62|The system must have a user manual and a FAQ section specifying how to use the non-admin features and a high-level overview of how the app works|Non-functional Documentation|Core|-|
|63|It should be possible to reconfigure the system, including changing the database name, login, and password|Non-functional Configuration management|Core|-|
|64|The system must have a 99.9% uptime|Non-functional Availability|Core|-|
|65|User data stored by the system should be encrypted at rest|Non-functional Security|Core|-|
