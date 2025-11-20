# Overview

ServiçosPro is a service marketplace platform inspired by GetNinjas and Thumbtack, connecting clients with service professionals in Brazil. The platform enables clients to search for professionals by category and location (using Brazilian CEP postal codes), request service quotes, and leave reviews. Professionals can create profiles showcasing their services, respond to client requests, and build their reputation through ratings.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Web Framework
- **Flask** - Lightweight Python web framework serving as the application foundation
- **Jinja2 Templates** - Server-side rendering for all user-facing pages
- **Flask-Login** - Session-based authentication managing user login state
- **Werkzeug** - Password hashing (generate_password_hash, check_password_hash) for secure credential storage

## Database Layer
- **SQLAlchemy ORM** - Database abstraction with declarative models
- **Flask-SQLAlchemy** - Flask integration for SQLAlchemy
- **Connection Pooling** - Configured with pool_recycle (300s) and pool_pre_ping for reliability
- **Database URI** - Sourced from DATABASE_URL environment variable (database-agnostic)

## Data Models
Core entities with relationship mappings:
- **User** - Stores credentials, contact info, and Brazilian address data (CPF, CEP, city, state)
- **Professional** - Extended profile linked to User, includes bio, pricing, verification status
- **ServiceCategory** - Predefined service types (e.g., "Reformas e Reparos", "Tecnologia")
- **ServiceRequest** - Quote requests from clients to professionals (implied from routes/templates)
- **Review** - Client ratings and comments for professionals (implied from routes/templates)

Relationships use cascade delete-orphan for data integrity.

## Authentication & Authorization
- **User Types** - Dual-mode system: "client" (service seekers) and "professional" (service providers)
- **Session Management** - Flask-Login with secret key from SESSION_SECRET environment variable
- **Password Security** - Werkzeug hashing (no plaintext storage)
- **Login Required** - Decorators protect dashboard and profile management routes

## Frontend Architecture
- **CSS Framework** - Custom CSS with CSS variables for theming (Tailwind-inspired utility approach per design_guidelines.md)
- **Typography** - Inter font family via Google Fonts CDN
- **Component System** - Reusable template components: navbar, hero, cards, forms
- **Responsive Design** - Mobile-first approach with breakpoint-based layouts
- **Icons** - Font Awesome 6.4.0 for UI iconography

## Location Services
- **CEP Validation** - Integration with ViaCEP API (viacep.com.br) for Brazilian postal code lookup
- **Address Autocomplete** - Client-side JavaScript fetches address data from CEP input
- **Geographic Filtering** - Search functionality filters professionals by city/state

## Validation
- **CPF Validation** - validate-docbr library ensures Brazilian tax ID format compliance
- **Form Validation** - Server-side validation in routes with flash message feedback
- **CEP Format** - Strips formatting (dots/hyphens) and validates 8-digit format

## Application Structure
- **app.py** - Application factory, database initialization, login manager configuration
- **models.py** - SQLAlchemy model definitions
- **routes.py** - Request handlers for all endpoints (registration, search, profiles, requests)
- **main.py** - Application entry point
- **seed_data.py** - Database seeding script for categories and sample professionals

## User Flows
1. **Client Flow**: Register → Search professionals by category/location → Request quote → Review professional
2. **Professional Flow**: Register → Complete profile (category, bio, pricing) → Receive requests → Respond to clients
3. **Shared**: Dashboard views customized by user type (dashboard_client.html vs dashboard_professional.html)

# External Dependencies

## Third-Party APIs
- **ViaCEP API** (viacep.com.br/ws/{cep}/json/) - Brazilian postal code to address resolution, 5-second timeout, handles error responses

## Python Libraries
- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM integration
- **Flask-Login** - Authentication
- **Werkzeug** - Security utilities (password hashing, ProxyFix middleware)
- **validate-docbr** - Brazilian document validation (CPF)
- **requests** - HTTP client for ViaCEP integration

## Frontend Libraries
- **Google Fonts** - Inter font family (weights: 400, 500, 700)
- **Font Awesome 6.4.0** - Icon library via CDN

## Environment Variables
- **SESSION_SECRET** - Flask session encryption key
- **DATABASE_URL** - Database connection string (supports PostgreSQL, MySQL, SQLite via SQLAlchemy)

## Infrastructure
- **ProxyFix Middleware** - x_proto and x_host headers for reverse proxy compatibility (Replit deployment)
- **Database Connection Pooling** - Auto-reconnection and stale connection handling for cloud database reliability