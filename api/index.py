"""
Vercel Serverless Function entry point.
Wraps the Flask app for Vercel's Python runtime.
"""
import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import create_app

app = create_app()
