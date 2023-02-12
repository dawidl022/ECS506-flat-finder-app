# Flat Finder app Requirements

|ID|Requirement|Type|Priority|Use Case|
|--|-----------|----|--------|--------|
|1 |Each user must be identified with their corporate email address|Functional (D)|Core|-|
|2 |The system must have two types of users: consultant and system administrator.|Functional|Core|-|
|3 |Only admins should be able to access the admin portal|Functional|Core|-|
|4 |The system should periodically fetch listings from external APIs and update the listings catalogue in the system|Functional|Core|-|
| |Users will log in using Single Sign On (SSO) with their corporate accounts|Functional|Core|Login|
| |Users will be registered in the system the first time they log in using Single Sign On|Functional|Core|Login|
| |Upon first logging into the system, consultants should be prompted to complete their profile (Work site, Slack member ID, optional photo)|Functional (D)|Core|Complete Profile|
| |Profiles can be completed later by any type of user, but no listing may be posted without a complete profile|Functional|Core|Complete Profile|
| |Users must be able to logout|Functional|Core|Logout|
| |Admins should be able to view users registered in the system|Functional|Core|View users
| |Admins should be able to make other users admins, either by selecting from the list of users of by manually entering their corporate email address|Functional|Core|Make user admin|
| |Admins should be able to remove users from the system|Functional|Optional|Remove User|
| |Removing a user should delete all of their user data and listings, but preserve the contents of their reviews|Functional (D)|Optional|Remove User|
| |By default all external sources should be enabled|Functional|Core|Configure external sources|
| |Admins should be able to enable external sources for pulling listings|Functional|Optional|Configure external sources|
| |Admins should be able to disable external sources for pulling listings|Functional|Optional|Configure external sources|
| |Disabling an external source should hide all listings from that source from non-admin users and pause automatic pulling of listings from that source|Functional|Optional|Configure external sources|Functional|Delete Listing|
| |Users should be able to view all non-hidden listings in the system|Functional|Core|View Listings|
| |Admins should be able to view listings from disabled external sources which should be clearly labelled as "Hidden"|Functional|Optional|View Listings|
| |Listings should be paginated|Functional|Core|View Listings|
| |Each accommodation listing in the list must have a title, photo, brief description, rating, source, price, distance from the specified location, postal code, accommodation type, "favourite" indicator|Functional (D)|Core|View Accommodation Listings|
| |Each seeking listing in the list must have title, brief description, distance from specified location, "favourite" indicator|Functional (D)|Core|View Seeking Listings|
| |Seeking listings should be sorted by distance from specified location|Functional|Core|View Seeking Listings|
| |Admins should be able to remove any listings from the system|Functional|Core|Remove Listing|
| |Users should be prompted to specify the location they wish to search near to, and select a maximum distance from this location|Functional|Core|Filter Listings|
| |Users should have the option of filtering accommodation listings by maximum distance from specified location|Functional|Optional|Filter Accommodation Listings
| |Users should have the option of filtering accommodation listings by source (internal/external/both)|Functional|Optional|Filter Accommodation Listings|
| |Users should have the option of filtering accommodation listings by maximum price|Functional|Optional|Filter Accommodation Listings|
| |Users should be able to sort accommodation listings by price|Functional|Core|Sort Accommodation Listings|
| |Users should be able to sort accommodation listings by distance from the specified location|Functional|Core|Sort Accommodation Listings|
| |Users should be able to enter a detailed view of a selected listing from the search results|Functional|Core|View Listing Details|
| 32|The detailed accommodation listing view must have a title, full description, gallery of photos, rating, source, price breakdown, full address, number of rooms, contact information, link to the original external listing (if applicable)|Functional|Core|View Accommodation Listing Details|
| 33|The detailed seeking accommodation listing view must have a title, full description, contact information and preferred location|Functional|Core|View Seeking Listing Details|
| |Users should be able to return from a detailed listing view to where they were in the search results|Functional|Core|View Listings|
| |Users should have the option of adding a listing to their favourites|Functional|Optional|Add Listing to Favourites|
| |Users should have the option of viewing their favourited listings|Functional|Optional|View Favourite Listings|
| |Users should have the option of removing a listing from their favourites|Functional|Optional|Remove Listing from Favourites|
| |Users should be able to leave a textual review along with a rating (0-5) on any accommodation listing|Functional|Optional|Leave Review|
| |Users should be able to leave a textual review along with a rating (0-5) on any listing author|Functional|Optional|Leave Review|
| |Users should be able to create listings about an accommodation, providing all the details specified in RQ32|Functional|Core|Create Accommodation Listing|
| |When creating an accommodation listing, users should be able to upload 0-15 photos|Functional (D)|Core|Create Accommodation Listing
| |Users should be able to create listings about seeking accommodation, providing all the details specified in RQ33|Functional|Core|Create Seeking Listing|
| |Users should be able to view the profiles of other users that have posted a listing|Functional|Core|View Profile|
| |User profiles should show their name, optionally a photo, the site they currently work at and links to their corporate chat (Slack/Teams)|Functional (D)|Core|View Profile|
| |Admins should be able to enable/disable corporate chat integrations (Slack/Teams)|Functional|Optional|Administrate Chat Integrations|
| |The system must not allow performing any activities without authentication|Non-functional Security|Core|-|
| |The database should be backup up once per day|Non-functional Backup|Core|-|
| |he application should comply with the Web Content Accessibility Guidelines (WCAG) 2.1 level AA|Non-functional Accessibility|Core|-|
