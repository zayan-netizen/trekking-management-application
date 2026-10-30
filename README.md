# Trekking Management Application

Secured **A grade** for web-based Trekking Management Application developed as part of the **IIT Madras BS Degree – Modern Application Development I (MAD1)** project.

The application provides a centralized platform for managing trekking activities through three distinct user roles: **Admin, Staff, and User**. Each role has specific permissions and functionalities to ensure efficient management of treks, staff assignments, and participant bookings.

## Technology Stack

| Technology | Purpose |
|---|---|
| HTML | Structuring web pages |
| CSS | Styling and UI design |
| JavaScript | Client-side functionality |
| Python | Backend programming |
| Flask | Web framework and application logic |

## Features

The application implements role-based access control, providing different functionalities depending on the user's role.

### 1. Administrator

The administrator has overall control of the application and is responsible for managing treks, users, and staff.

- **Trek Management:** Create new treks, view existing treks, edit trek details, and manage trek availability.
- **User Management:** View and manage registered users.
- **Staff Management:** Manage staff accounts and approve or reject staff registration requests.
- **Staff Assignment:** Assign specific treks to staff members for management.
- **Administrative Control:** Oversee trekking activities and manage the application through the admin dashboard.

### 2. User

Registered users can explore available trekking activities and manage their bookings.

- **Browse Treks:** View available treks and their details.
- **Book Treks:** Reserve a spot on a trek.
- **Cancel Bookings:** Cancel previously made trek reservations.
- **Booking Management:** Manage their trekking reservations through their dashboard.

### 3. Staff

Staff members are responsible for managing the treks assigned to them by the administrator.

- **Assigned Trek Management:** View and manage only the treks assigned to them.
- **Participant Management:** View and manage participants registered for their assigned treks.
- **Restricted Access:** Staff members can access only their assigned trekking activities and related participant information.
- **Approval-Based Login:** Staff accounts require administrator approval before they can access the application.

## Screenshots

### Application Interface

![Application Screenshot](static/Screenshot%20(240).png)

### Initial UI

![Initial UI](static/initial.png)

The initial design relied heavily on cards to display information. Although functional, the interface felt cluttered.

### Final UI

![Final UI](static/final.png)

I redesigned the interface by reducing unnecessary card components and simplifying the overall layout, resulting in a cleaner and more consistent user experience.

## Running the Application

### 1. Clone or Download the Repository

Download the repository or clone it using Git.

### 2. Navigate to the Project Directory

Open a terminal or Command Prompt and navigate to the root directory containing `app.py`.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Application

```bash
python app.py
```

### 5. Access the Application

Open the following URL in your browser:

```text
http://127.0.0.1:5000
```

## Default Administrator Credentials

The application comes with a pre-configured administrator account.

| Field | Credentials |
|---|---|
| Username | `akzayan8` |
| Password | `akzayan8` |

**Changing Administrator Credentials**

You can modify the default administrator username and password in `create_admin.py`.

**Important:** If the application has already been initialized, delete the `instance` folder before running it again with the updated credentials. This resets the existing database, and all previously stored application data will be lost.

## Challenges and Lessons Learned

### 1. Understanding Decorators and Wrapper Functions

One of my initial challenges was implementing role-based access control.

I needed to restrict certain routes based on whether the logged-in user was an administrator, staff member, or regular user.

To achieve this, I explored Python decorators and wrapper functions and implemented custom decorators to control access to protected routes.

This helped me understand how decorators work internally and how they can be used to avoid repeating authentication and authorization logic across multiple routes.

### 2. Flask Sessions and Cookie Management

After implementing route protection, I encountered an unexpected issue: even after restarting the Flask server, the browser continued redirecting me to the user dashboard without requiring another login.

After investigating the issue, I learned that browser cookies and session information can persist across server restarts.

I addressed this by implementing logout functionality that clears the user's session.

This gave me a better understanding of how Flask sessions, cookies, and authentication work together.

### 3. Handling Shared Templates and Dynamic Variables

Another challenge occurred while developing the profile page, which was shared by administrators, staff, and regular users.

The staff profile required additional form fields that were not applicable to administrators or regular users.

Since the same template was being used for different roles, passing undefined variables to `render_template()` resulted in errors.

I resolved this by ensuring that all expected template variables were defined, providing appropriate default values where certain fields were not required.

### 4. Managing Role-Based Pages and Shared Components

I also faced difficulties configuring pages and templates shared between administrators and staff.

Although both roles used similar interfaces, their permissions, available actions, and required data were different.

Handling these differences while maintaining reusable templates required several iterations and debugging.

This experience helped me understand the importance of separating role-specific logic from shared application components.

## What I Learned

Working on this project helped me gain practical experience in:

- Backend development using Python and Flask.
- Structuring web pages using HTML and CSS.
- Adding client-side functionality using JavaScript.
- Managing application data and database operations.
- Implementing authentication and role-based authorization.
- Understanding Python decorators and wrapper functions.
- Working with Flask sessions and cookies.
- Designing reusable templates for different user roles.
- Debugging and improving application architecture.
