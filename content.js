/*
 * ============================================================
 *  EDIT THIS FILE ONLY. Everything on the site comes from here.
 * ============================================================
 *  - Put your photos in the /images folder and reference them below.
 *  - Any image that is missing shows a grey placeholder, so the
 *    site never looks broken while you collect photos.
 *  - Leave a value as "" to hide that line.
 */
window.PORTFOLIO = {
  name: "Sanchay Kumar",
  tagline: "Model · Based in [City]",       // e.g. "Model · Chennai / Mumbai"
  bio: "Write 2–3 sentences: where you're based, what kind of work you do (editorial, commercial, fitness, runway), and whether you're available to travel. Keep it short — clients look at photos, not paragraphs.",
  digitalsUpdated: "Nov 2026",             // keep digitals less than ~3 months old

  // Measurements. Be exact — clients and agencies check these on set.
  stats: [
    ["Height", "—"],                       // e.g. "185 cm / 6'1\""
    ["Chest", "—"],
    ["Waist", "—"],
    ["Hips", "—"],
    ["Shoe", "—"],
    ["Hair", "—"],
    ["Eyes", "—"],
  ],

  // Your book. Order matters: put your 3 strongest images first.
  // category must be one of the names in `categories`.
  categories: ["All", "Editorial", "Commercial", "Runway"],
  book: [
    { src: "images/book-01.jpg", category: "Editorial",  credit: "Photo: Name · Styling: Name" },
    { src: "images/book-02.jpg", category: "Commercial", credit: "Photo: Name · Client: Brand" },
    { src: "images/book-03.jpg", category: "Editorial",  credit: "Photo: Name" },
    { src: "images/book-04.jpg", category: "Runway",     credit: "Show: Name, Season" },
    { src: "images/book-05.jpg", category: "Commercial", credit: "Photo: Name" },
    { src: "images/book-06.jpg", category: "Editorial",  credit: "Photo: Name" },
    { src: "images/book-07.jpg", category: "Commercial", credit: "Photo: Name" },
    { src: "images/book-08.jpg", category: "Editorial",  credit: "Photo: Name" },
  ],

  // Digitals / polaroids: plain background, fitted clothes, no makeup.
  digitals: [
    { src: "images/digital-front.jpg",   label: "Front" },
    { src: "images/digital-profile.jpg", label: "Profile" },
    { src: "images/digital-full.jpg",    label: "Full length" },
    { src: "images/digital-back.jpg",    label: "Back" },
  ],

  experience: [
    "Brand / client — type of job, year",
    "Show / designer — runway, year",
    "Magazine — editorial, year",
  ],
  skills: ["Runway", "Commercial print", "Fitness", "On-camera / video"],

  // Contact. Use a dedicated booking email, not your personal one.
  // If you sign with an agency, put the agency first.
  contact: [
    { label: "Booking", value: "booking@example.com", href: "mailto:booking@example.com" },
    { label: "Instagram", value: "@yourhandle", href: "https://instagram.com/yourhandle" },
    { label: "Agency", value: "", href: "" },
  ],

  compCard: "compcard.pdf",                // set to "" to hide the button
};
