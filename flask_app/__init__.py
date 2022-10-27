from flask import Flask, render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.secret_key = "any string you want"

bcrypt = Bcrypt(app)
