﻿# Work Process Tracking System
 This project is a Work Process Tracking System built with Django, inspired by Trello. It allows organizations to manage projects (boards) and track work processes through draggable lists and cards. The app is designed for teams to collaborate efficiently by creating and managing tasks within boards.

# WebApp Images
![image](https://github.com/user-attachments/assets/f279ac0c-d5be-47dc-a640-d2155d2ca997)
![image](https://github.com/user-attachments/assets/a6fbd974-5288-476e-88df-05b18517cfb5)
![image](https://github.com/user-attachments/assets/556e24e2-eb86-40fe-908d-cf484d815a06)
![image](https://github.com/user-attachments/assets/fc7f56d7-3d21-4d93-a7a1-3748add1c6b9)





# Features
1) User Authentication: Organizations can create accounts and add team members, who receive their credentials via email.
2) Board Management: Create multiple boards (projects) and assign team members to specific boards.
3) Card and List Management: Within each board, users can create cards and organize tasks by creating draggable lists.
4) Role-Based Access: Users only see the boards they are assigned to, ensuring focused work environments.

# Technologies Used
1) Backend: Django
2) Frontend: HTML, CSS, Bootstrap 4, JavaScript
3) Database: SQLite (default, can be changed)
4) Email Service: Django's Email backend (for sending passwords)

# Installation
1) Clone the Repository: git clone https://github.com/mudassirzeya/track_your_process_status.git
2) Create a Virtual Environment (It's recommended to use a virtual environment to manage dependencies).
   1. python3 -m venv venv
   2. source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3) Install Dependencies
   1. pip install django
   2. pip install pillow
4) Configure the Database (By default, the app uses SQLite. You can configure another database in the settings.py file) .
   1. python manage.py migrate
5) Set Up Email Backend
   1. Update the email configuration in the settings.py file to use your preferred email service for sending passwords.
6) Create Superuser (Admin Account): python manage.py createsuperuser
7) Run the Development Server: python manage.py runserver

# Usage
### For Organizations:
1. Sign up for a new account.
2. Create boards (projects) and assign team members.
3. Team members receive login credentials via email.
### For Team Members:
1. Log in with the credentials sent via email.
2. Access only the boards you’re assigned to.
3. Create cards and organize tasks by creating draggable lists within each board.
### For Admins:
1. Manage boards, team members, and monitor progress across projects.

# Contributing
Contributions are welcome! Please submit a pull request or open an issue to contribute to this project.
