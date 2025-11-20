# Design Guidelines: GetNinjas-Style Marketplace Platform

## Design Approach
**Reference-Based:** Drawing inspiration from GetNinjas, Thumbtack, and modern service marketplaces that balance trust-building with conversion optimization.

**Core Principles:**
- Professional trustworthiness with approachable aesthetics
- Clear service discovery and professional showcasing
- Streamlined request/hiring flow
- Location-based relevance (CEP integration)

## Typography
**Font Stack:**
- Primary: Inter (via Google Fonts CDN) - clean, modern, excellent readability
- Headings: 700 weight
- Body: 400 weight
- Subtext/labels: 500 weight

**Hierarchy:**
- H1: text-4xl lg:text-5xl font-bold
- H2: text-3xl lg:text-4xl font-bold
- H3: text-2xl font-bold
- Body: text-base
- Small/meta: text-sm

## Layout System
**Spacing Primitives:** Use Tailwind units of 2, 4, 6, 8, 12, 16, 20, 24
- Component padding: p-4 to p-8
- Section spacing: py-12 lg:py-20
- Card gaps: gap-6
- Form spacing: space-y-4

**Container Strategy:**
- Max width: max-w-7xl mx-auto px-4
- Content sections: max-w-6xl
- Forms: max-w-md

## Component Library

### Navigation
- Fixed header with logo, search bar (prominent), category links, auth buttons
- Mobile: Hamburger menu with full-screen overlay
- Include "Seja um Profissional" CTA button (distinct styling)

### Hero Section
- Full-width background with professional service imagery (people working, professionals)
- Centered search interface overlay with blurred background
- Search includes: service type dropdown + CEP input + CTA button
- Text: H1 headline + supporting subtext
- Height: min-h-[500px] lg:min-h-[600px]

### Service Categories Grid
- 3-column grid (lg:grid-cols-3 md:grid-cols-2 grid-cols-1)
- Icon + category name cards
- Hover state: subtle lift effect (transform: translateY(-4px))

### Professional Cards
- Grid layout: lg:grid-cols-3 md:grid-cols-2
- Card includes: profile photo (rounded), name, service category, rating stars, review count, location (by CEP), starting price, "Ver Perfil" button
- Spacing: p-6, gap-4

### Profile Pages
- Two-column layout on desktop (8/4 split)
- Left: Profile photo, bio, services offered, portfolio/images grid, reviews section
- Right: Sticky sidebar with pricing card, "Solicitar Orçamento" form, response time, verification badges
- Mobile: Stack vertically

### Forms (Auth & Requests)
- Single column, centered: max-w-md
- Input fields: Full-width with border, rounded-lg, p-3
- CPF input: Include mask formatting (###.###.###-##)
- CEP input: Auto-complete address lookup
- Primary buttons: w-full, py-3, rounded-lg
- Spacing: space-y-4 between fields

### Dashboard Panels
- Sidebar navigation (fixed on desktop, collapsible on mobile)
- Content area with cards for: active requests, messages, profile stats
- Table views for request management with status badges

### Request/Quote System
- Modal or dedicated page with multi-step form
- Steps: Service details → Schedule preference → Budget → Review & Submit
- Progress indicator at top

### Reviews Section
- Star rating display (use Font Awesome icons via CDN)
- Review cards with: user avatar, name, rating, date, comment text
- "Mostrar mais" pagination

### Trust Elements
- Verification badges: "CPF Verificado", "Perfil Completo"
- Security icons near sensitive inputs (CPF, payment)
- "Como funciona" section with numbered steps

### Footer
- Multi-column layout: About, Categories, Support, Social
- Newsletter signup form
- Trust badges: "Seguro", "Privacidade Garantida"
- Copyright and legal links

## Icons
**Library:** Font Awesome (via CDN)
- Search, location, star ratings, checkmarks, shields (trust), user profile, category icons

## Images
**Required Images:**
1. **Hero:** Professional service worker in action (plumber, electrician, cleaner) - warm, trustworthy photography
2. **Category Icons:** Use Font Awesome for service categories (wrench, paint-roller, laptop, etc.)
3. **Professional Profiles:** Placeholder for user-uploaded photos (use avatar placeholders)
4. **Trust Section:** Illustration or photo showing platform benefits

**Placement:**
- Hero: Background image with gradient overlay for text readability
- Service cards: Small icon representations
- Professional cards: Profile photos (rounded-full, 80x80px minimum)

## Responsive Behavior
- Mobile-first approach
- Breakpoints: md (768px), lg (1024px)
- Stack columns vertically on mobile
- Full-width search on mobile, inline on desktop
- Collapsible filters for search results on mobile

## Accessibility
- High contrast between text and backgrounds
- Form labels always visible
- Focus states on all interactive elements
- Alt text for all images
- Semantic HTML structure

## Key UX Patterns
- Sticky header for easy navigation
- Breadcrumbs on detail pages
- Loading states for CEP lookup
- Error messages inline with form fields
- Success confirmations after actions (green banner)
- Empty states with helpful CTAs

This design creates a trustworthy, conversion-focused marketplace that prioritizes easy service discovery and professional credibility while maintaining the Brazilian market context with CPF/CEP integration.