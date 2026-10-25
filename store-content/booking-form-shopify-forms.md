# Booking form: set up with Shopify Forms

Shopify doesn't let apps or the API create Shopify Forms, so this form has to be made in the Forms app. It takes about 10 minutes.
Once it's on the page, every booking is saved in Shopify admin (Customers, and Apps → Forms → Submissions) and you get an email for each one.

Hours: **Monday to Saturday, 4:30 pm to 9 pm. Closed Sunday.**

## 1. Create the form

1. Go to Shopify admin → **Online Store → Themes → Customize** on the live theme.
2. Open the page selector at the top and choose **Pages → Book a Showroom Visit** (template `book-appointment`).
3. In the left panel, under the **ETS showroom booking** section, click **Add block → Apps → Form (Shopify Forms)**.
4. Click **Create form**, then choose **Inline** and start from a blank or contact template.

## 2. Fields to add (in this order)

| Field | Type | Required | Options / notes |
| --- | --- | --- | --- |
| Appointment type | Dropdown | Yes | Showroom visit · Tile & bathroom selection · Tiling quote or project chat · Collect an online order |
| Preferred date | Date (or short text "e.g. Tue 30 Sep") | Yes | Help text: "Monday to Saturday only. We're closed Sunday." |
| Preferred time | Dropdown | Yes | 4:30 pm · 5:00 pm · 5:30 pm · 6:00 pm · 6:30 pm · 7:00 pm · 7:30 pm · 8:00 pm · 8:30 pm |
| Another time that suits | Short text | No | Placeholder: "e.g. Any weekday after 6 pm" |
| First name / Last name | Name | Yes | |
| Email | Email | Yes | |
| Phone | Phone | Yes | |
| Suburb | Short text | No | |
| Order number (if collecting) | Short text | No | |
| Anything we should know? | Long text | No | |
| Email marketing | Checkbox | No | Leave unticked by default |

If the Forms app has no Date field, use a Short text field.

## 3. Form settings

- **Heading:** Request an appointment
- **Description:** Appointments Monday to Saturday, 4:30 pm to 9 pm. Choose a time and we'll confirm by phone or email.
- **Button:** Request appointment
- **Success message:** Thanks, we've received your booking request. We'll contact you to confirm your appointment. Your time isn't locked in until we confirm it. If it's urgent, call 0450 960 543.
- **Customer tags:** `booking-request`, so you can filter bookings in Customers.
- **Notifications:** turn on staff email notifications to contactus@excellenttilingservices.com.
- **Colours** (to match the site): text `#1F3153`, button `#1F3153`, button label `#FFFFFF`, links `#1F3153`, errors `#E02229`. Alignment left.

## 4. Publish

1. Click **Save** in the Forms editor, then **Save** in the theme editor.
2. When a Forms block is present, the built-in request form is hidden automatically, so there's never two forms on the page.
3. Send a test booking and check it appears under **Customers** (tag `booking-request`) and that the email arrives.

## Handling a booking

The form takes requests. It doesn't block out times, so two people could ask for the same slot. Reply to confirm, or offer another time. Filter Customers by the `booking-request` tag to see every request.
