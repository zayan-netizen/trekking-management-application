### Trekking Management Application

- The Trekking Management Application is being developed as a college project to demonstrate the application of software engineering principles, database management, and web application development. 

- The project aims to provide a digital solution for managing trekking-related activities that are traditionally handled through manual processes. By developing this system, students gain practical experience in designing user-friendly interfaces, implementing business logic, managing data efficiently, and integrating various software components into a complete application. 

- The project serves as a real-world example of how technology can be used to improve organization, accessibility, and efficiency in activity management systems.

#### Problems I faced

- I had a very difficult time in understanding decorators and wrapper functions, to restrict activity based on roles. So I had to study about
decorators and wrappers, then write a function.

- Even after writing the decorator and applying it before the route to user_dashboard, even without logging in, it was redirecting to the user dashboard, I looked it up then I understood that the browser saves the cookies still the next time, so even tho I ended the server and restarted it, it was still redirecting, so I had to create a logout function which clear the sessions.

