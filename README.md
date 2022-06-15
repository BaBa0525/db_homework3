# Introduction to Database Systems Homework 3

> Topic: Food Ordering Service part.2 <br>
> Deadline: 2022/06/17 23:59

## Initialization

```sh
zsh init.zsh
```

## Frontend

We use <code>npm</code> + Vite this time.

<strong>TODOs</strong>

Pages:
- [x] Index
    - [x] Login Page
    - [x] Registration Page
- [ ] Home 
    - [ ] Navigation Sidebar { BaBa }
        - [ ] Recharge
    - [ ] Search Page { Alan }
        - [ ] Menu
    - [x] Shop Management Page
        - [x] Shop Registration
        - [x] Shop Meals Editing
    - [ ] User Order Page
        - [ ] Order Detail
    - [ ] Shop Order Page
        - [ ] Order Detail
    - [ ] Transaction Page

Components:
- [x] Base Input
- [x] Base Drop Down
- [x] Base Form (Row / Column)
- [x] Base Table
- [x] Popup Window

## Backend

### Package Structure

```
├── ordering/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── requestRoute/
│   │   ├── __init__.py
│   │   ├── mealRoutes.py
│   │   ├── shopRoutes.py
│   │   └── userRoutes.py
│   └── schema.py
└── run.py
```
