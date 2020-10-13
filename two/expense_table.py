from flask import Flask, jsonify, redirect, render_template, request, session, logging, url_for, redirect, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt
from datetime import datetime
import os


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

