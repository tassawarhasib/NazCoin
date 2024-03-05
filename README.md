# NAZCOIN🪙
<p align="center"><img src="static/assets/img/favicon.png" /></p>
The project aims at building its own cryptocurrency from scratch using block chain technology. The project uses Python language along with Flask Frameworks to deploy it on a localhost server. This project therefore not only gets us to know about block chain, encryptions and keys but also brings us closer to the world of cryptocurrency whose value is increasing day by day in the modern era.

## 📃Table Of Contents
* [Introduction](#introduction)
  * [About Project](#about-project)
  * [Tech-Stack](#tech-stack)
  * [File Structure](#file-structure)
* [Getting Started](#getting-started)
  * [Pre-requisites](#pre-requisites)
  * [Usage](#usage)
* [Glimpses](#Glimpses)
* [Google Drive Link](#gdrive)
* [Trouble Shooting](#trouble-shooting)
* [Future Scope](#future-scope)
* [Contributors](#contributors)
* [Mentors](#mentors)

## 🙂Introduction
Introducing Naz Coin, our cryptocurrency in development. Fueled by cutting-edge blockchain technology, Naz Coin aims to redefine digital transactions. With a focus on security, efficiency, and user-friendly features, we're crafting a cryptocurrency poised to revolutionize the way we engage with digital assets. Stay tuned for an innovative and seamless financial experience.

### 🤔About Project
Our aim with Naz Coin is to pioneer a user-centric cryptocurrency on the blockchain, prioritizing security, efficiency, and accessibility. We strive to empower users with a seamless digital currency experience, leveraging blockchain technology to ensure transparency, decentralization, and a robust foundation for the future of financial transactions.

### ⚙️Tech-Stack

<h5>FRONTEND</h5>

- ```HTML```
- ```CSS```
- ```Bootstrap``` 
- ```Javascript```

<h5>BACKEND</h5>

- ```Python```
- ```Flask```
- ```MySQL``` 


### 📁File Structure
```
NazCoin
├───.idea
│   └───inspectionProfiles
├───static
│   └───assets
│       ├───bootstrap
│       │   ├───css
│       │   └───js
│       ├───css
│       ├───fonts
│       ├───img
│       │   ├───bg
│       │   ├───blog
│       │   ├───board
│       │   ├───icon
│       │   ├───partner
│       │   ├───portfolio
│       │   ├───team
│       │   └───testimonial
│       ├───js
│       └───owlcarousel
│           ├───css
│           └───js
├───templates
│   ├───handlers
│       ├───404.html
│   └───includes
│       ├───404.html
│        ├───404.html
│   ├───buy.html
│   ├───dashboard.html
│   ├───index.html
│   ├───layout.html
│   ├───login.html
│   ├───register.html
│   ├───transaction.html
│
├───app.py
├───blockchain.py
├───forms.py
├───sqlhelpers.py
├───requirements.txt
├───readme.md
 ```
## ⚒️Getting Started

### 😁Pre-requisites
The project involes the installation of following libraries and environment:
* Firstly obviously you should have [Python3](https://www.python.org/downloads/).
* Some basic libraries and frameworks will come pre-installed but you'll require MORE!!
* [Flask](https://flask.palletsprojects.com/en/2.0.x/): This the the framework that supports the website so installing this is a must else it'll throw ERRORS!!
* [Requests](https://pypi.org/project/requests/): This module is used only once :(, but none the less it is important.
* [An SQL connection with Flask](https://flask-mysqldb.readthedocs.io/en/latest/): This library ensures a connection between the MySQL Database and the Flask framework.
* wtforms: A python library used for getting inuput from a user in forms

Install all these requirements:
```
$ pip install -r requirements.txt
```
* After install Mysql on your PC open your prompt and type:
  ```
  $ mysql -u root -p
  ```
  and enter the password
* After follow thw following steps:
  ```
  $ CREATE DATABASE crypto;
  ```
  ```
  $ USE crypto;
  ```
  ```
  $ CREATE TABLE users(name varchar(50), email varchar(30), username varchar(30), password varchar(100));
  ```
  ```
  $ CREATE TABLE port5000(number varchar(10), hash varchar(64), previous varchar(64), sender varchar(30), recipient varchar(30, amount varchar(30), nonce varchar(20));
  ```
  ```
  $ CREATE TABLE port5001(number varchar(10), hash varchar(64), previous varchar(64), sender varchar(30), recipient varchar(30, amount varchar(30), nonce varchar(20));
  ```
  This is for 2 ports, for multiple ports make multiple tables and thus make changes in the list of connected tables in the app.py file accordingly
  
## 💻Usage
Assuming you have git, follow the following process
1. Clone the Git Repo:
   ```
   $ git clone https://github.com/NAZCOIN.git
   ```
2. Go into the Repo directory
   ```
   $ cd ../NAZCOIN
   ```
   
4. Run the `app.py` file in the directory with a port number
   ```
   $ python app.py 5000
   ```
5. Run `app.py` again but this time witha different port number, 5001
   ```
   $ python app.py 5001
   ```
7. 2 local-host server address will open on the 2 different terminals
   ![image](https://user-images.githubusercontent.com/84843295/150394240-fc791e9f-db2f-47c5-9364-36a116bae684.png)
   ![image](https://user-images.githubusercontent.com/84843295/150394392-72d2a8aa-5dc4-44a5-aa2a-44ff5773139b.png)
   
8. Register 2 accounts on the 2 different ports and thus there 2 ports become 2 different users. For more users make more tables and add them in the list of connected users in app.py

9. Now show this to your friends and boast about how you've created your own crypto-currency and that you're going to become a millionaire🤑


## 😵‍💫Trouble Shooting
The making of this project tackled numerous obstacles. Some were tricky, while some were very easy to solve.
1. The first problem faced was that the **team was not working** 🙂. This was the most tough and complex problem to solve since each member had to come out of their comfort zone and contribute.
2. **Installations**: The various modules to be installed keep getting updates regularly and so does their way of working, so managing to work with different versions of the same package/module was tricky indeed.
3. **Understanding**: Understanding Block-Chain, i.e getting its intuition at first was a bit difficult but eventually as we progressed the concept was well **inherited**.
4. **Programming**: Some of the members were seeing some new python syntax's and how to use the different modules.
5. **Debugging**: No comments.
6. **Choosing a good website design**: Choosing this was so tough that we try to keep adding new features regularly.
7. **Deploying the blockchain**: To deploy it on a server was not possible since blockchain is de-centralized, therefore for this SQL Tables were used for each user.


## 🔮Future Scope
Here are a few things we are planning on adding in the future
* Wallet
* Mempools
* The webdev part requires a lot more efforts and we'll try and implement that throught react.js

## 👨‍💻Contributors
* [Ritik Ranjan](https://github.com/ritikranjan12)
* [Tassawar Hasib](https://github.com/tassawarhasib)
* [Pintu Kumar Yadav](https://github.com/#)
* [Pravansu Sahoo](https://github.com/#)
## 🙏Mentors
A very special thanks to the mentors!!
* [Prof. Dr. LN Padhy](#)
* [Asst. Prof. Sigma Nayak](#)