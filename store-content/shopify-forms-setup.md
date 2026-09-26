# Shopify Forms: setting up every form on the site

The site has four forms. Each one works now using Shopify's built-in contact form, which only
**emails** each submission. Switching them to **Shopify Forms** means every submission is also
**saved** in Shopify admin as a customer (with tags and details) and under
Apps → Forms → Submissions.

Shopify doesn't let apps or the API create Shopify Forms, so each form is made once in the
Forms app, inside the theme editor. Every form section already has a slot for it. When a Forms
block is added, the built-in form hides automatically, so a page never shows two forms.

| Form | Page | Theme section | Customer tag |
| --- | --- | --- | --- |
| Trade account application | `/pages/trade-account` | ETS trade application | `trade-applicant` |
| Renovation / project quote | `/pages/request-a-quote` | ETS quote request | `quote-request` |
| Showroom booking | `/pages/book-appointment` | ETS showroom booking | `booking-request` |
| Contact | `/pages/contact` | ETS contact page | `contact-enquiry` |

## Before you start

1. Make sure the **Shopify Forms** app is installed: Shopify admin → Apps. If it isn't,
   install it free from the Shopify App Store.
2. Open the theme you'll publish: **Online Store → Themes → "ETS Rebuild 2026 (draft)" →
   Customize**.

## Adding a form (same steps for each)

1. In the page selector at the top of the editor, open the page (for example
   **Pages → Trade Account**).
2. In the left panel, click the form section (see the table), then **Add block → Apps →
   Form (Shopify Forms)**.
3. Click **Create form → Inline**, start from blank, and add the fields listed below.
4. Apply the **Form settings** and the **Style** below, then **Save** in Forms and **Save** in
   the theme editor.
5. Send a test submission. Check it appears in **Customers** with the tag and that the email
   notification arrives.

**Style (all forms, to match the site):** text `#15213A`, button background `#15213A`, button
label `#FFFFFF`, links `#9C7744`, error `#9B2C2C`, alignment left.

**Notifications (all forms):** turn on staff email notifications to
contactus@excellenttilingservice.com.au.

Leave **email marketing** unticked by default on every form.

---

## 1. Trade account application

| Field | Type | Required | Options / notes |
| --- | --- | --- | --- |
| Business name | Short text | Yes | Save to customer **Company** if offered |
| ABN | Short text | Yes | Help text: "11-digit ABN" |
| Trade type | Dropdown | Yes | Tiler · Builder · Plumber · Renovator / handyman · Waterproofer · Carpenter / cabinet maker · Interior designer · Property developer / investor · Other trade |
| Licence number | Short text | No | Help text: "Builder's, plumbing or other trade licence, if you hold one" |
| First name / Last name | Name | Yes | |
| Mobile | Phone | Yes | |
| Email | Email | Yes | Help text: "Use the email you'll log in with. Your trade prices are linked to it." |
| Estimated monthly spend | Dropdown | Yes | Under $1,000 · $1,000 – $5,000 · $5,000 – $15,000 · Over $15,000 |
| Mostly buying | Checkboxes | No | Tiles · Vanities & large items · Tapware & accessories |
| Delivery address | Address or short text | No | |
| Accounts email | Email / short text | No | "For invoices, if different" |
| Preferred payment | Dropdown | No | Card online at checkout · Bank transfer (EFT) · 30-day account (subject to approval) |
| Anything else? | Long text | No | |
| Confirmation | Checkbox | Yes | "I confirm these details are correct and I'm applying on behalf of a registered business." |

**Form settings**
- Heading: Apply for a trade account
- Button: Submit application
- Success message: Thanks, your trade application has been sent. We'll check your details and
  email you once your account is approved (usually within one business day). Then just log in
  with the same email address.
- Customer tags: `trade-applicant`

**Approving:** Customers → filter by tag `trade-applicant` → open the applicant → add the tag
**`trade`** → Save. Trade prices then show and apply at checkout when they log in. You can
remove `trade-applicant` once approved.

---

## 2. Renovation / project quote (free measure & quote)

| Field | Type | Required | Options / notes |
| --- | --- | --- | --- |
| What do you need? | Dropdown | Yes | Bathroom renovation · Kitchen or laundry · Tiling · Waterproofing / leak repair · Products only (supply) · Something else |
| Suburb | Short text | Yes | |
| Approximate size | Short text | No | "e.g. 2.4 × 3 m bathroom, or 25 m²" |
| Timing | Dropdown | No | As soon as possible · Within 1–3 months · 3–6 months · Just planning / getting prices |
| Property | Dropdown | No | My home · Rental / investment · New build · Commercial |
| Tell us about it | Long text | Yes | "What's there now, what you'd like, any products you've picked" |
| Photos or plans | File upload | No | If your Forms plan offers it; otherwise ask customers to email photos |
| First name / Last name | Name | Yes | |
| Phone | Phone | Yes | |
| Email | Email | Yes | |

**Form settings**
- Heading: Book a free measure & quote
- Button: Send enquiry
- Success message: Thanks, your enquiry has been sent. We'll be in touch to arrange your free
  measure and quote. Have photos or plans? Email them to
  contactus@excellenttilingservice.com.au with your name.
- Customer tags: `quote-request`

---

## 3. Showroom booking

Hours: **Monday to Saturday, 4:30 pm to 9 pm. Closed Sunday.**

| Field | Type | Required | Options / notes |
| --- | --- | --- | --- |
| Appointment type | Dropdown | Yes | Showroom visit · Tile & bathroom selection · Renovation or tiling quote · Collect an online order |
| Preferred date | Date (or short text "e.g. Tue 30 Sep") | Yes | Help text: "Monday to Saturday only. We're closed Sunday." |
| Preferred time | Dropdown | Yes | 4:30 pm · 5:00 pm · 5:30 pm · 6:00 pm · 6:30 pm · 7:00 pm · 7:30 pm · 8:00 pm · 8:30 pm |
| Another time that suits | Short text | No | "e.g. Any weekday after 6 pm" |
| First name / Last name | Name | Yes | |
| Email | Email | Yes | |
| Phone | Phone | Yes | |
| Suburb | Short text | No | |
| Order number (if collecting) | Short text | No | |
| Anything we should know? | Long text | No | |

**Form settings**
- Heading: Request an appointment
- Description: Appointments Monday to Saturday, 4:30 pm to 9 pm. Choose a time and we'll
  confirm by phone or email.
- Button: Request appointment
- Success message: Thanks, we've received your booking request. We'll contact you to confirm
  your appointment. Your time isn't locked in until we confirm it. If it's urgent, call
  0450 960 543.
- Customer tags: `booking-request`

The form takes requests; it doesn't block out times. Reply to confirm, or offer another time.

---

## 4. Contact

| Field | Type | Required | Options / notes |
| --- | --- | --- | --- |
| I need help with | Dropdown | Yes | Tiles · Vanities, basins & baths · Tapware, showers & accessories · Renovation or tiling job · Trade account · Existing order · Other |
| First name / Last name | Name | Yes | |
| Email | Email | Yes | |
| Phone | Phone | No | |
| Your message | Long text | Yes | |

**Form settings**
- Heading: Send us a message
- Button: Send message
- Success message: Thanks for getting in touch. We'll reply as soon as we can, usually within
  one business day. For anything urgent, call 0450 960 543.
- Customer tags: `contact-enquiry`

---

## Finding submissions

- **Customers:** filter by the tag (`trade-applicant`, `quote-request`, `booking-request`,
  `contact-enquiry`). Each submission's answers are on the customer record.
- **Apps → Forms → Submissions:** every submission in one list, exportable to CSV.
