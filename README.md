### Trekking Management Application

- The Trekking Management Application is being developed as a college project to demonstrate the application of software engineering principles, database management, and web application development. 

##### First UI

<img src="static/initial.png" width="50%">

- Initial UI in which I used cards for everything, finally removed the cards and it looked better.

##### Final UI

<img src="static/final.png" width="50%">

#### Problems I faced

- I had a very difficult time in understanding decorators and wrapper functions, to restrict activity based on roles. So I had to study about decorators and wrappers, then write a function for decorators or to restrict access.

- Even after writing the decorator and applying it before the route to user_dashboard, even without logging in, it was redirecting to the user dashboard, I looked it up then I understood that the browser saves the cookies still the next time, so even tho I ended the server and restarted it, it was still redirecting, so I had to create a logout function which clears the sessions.

- Faced a issue in my profile page, which is common for all admin, staff and user. I used a form for the staff's which was not required for admin and user, it gave me error while going to admin or user profile because I was passing undefined variables in the render_template statement, so I had to define empty strings for all those variables even though it was not being used.

- Overall I had faced a lot of issues in configuaring pages which were shared by both admin and staff, it gave me a lot of errors.

