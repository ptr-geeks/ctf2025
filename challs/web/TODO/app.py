#!/usr/bin/env python3

import json
import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
import copy

app = Flask(__name__)
app.secret_key = os.urandom(32)

FLAG = os.environ.get('FLAG', 'PTR{fake_flag}')

class AppConfig:
    def __init__(self):
        self.debug_mode = False
        self.maintenance_mode = False
        self.admin_access = False
        self.feature_flags = {
            'advanced_analytics': False,
            'team_collaboration': True,
            'export_functionality': True,
            'notification_system': True,
            'third_party_integrations': False
        }
        self.api_keys = {}
        self.security_headers = True
        self.theme_settings = {
            'primary_color': '#667eea',
            'secondary_color': '#764ba2',
            'accent_color': '#f093fb'
        }

app_config = AppConfig()
todos_storage = {}
user_profiles = {}
teams_storage = {}
notifications_storage = {}

def merge_user_preferences(existing_prefs, new_prefs):
    if not isinstance(existing_prefs, dict):
        existing_prefs = {}
    if not isinstance(new_prefs, dict):
        return existing_prefs
    
    merged = copy.deepcopy(existing_prefs)
    
    for key, value in new_prefs.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_user_preferences(merged[key], value)
        else:
            merged[key] = value
    
    return merged

def apply_config_overrides():
    if 'config_overrides' in session:
        for attr, value in session['config_overrides'].items():
            if hasattr(app_config, attr):
                setattr(app_config, attr, value)

def generate_analytics_data():
    """Generate fake analytics data"""
    return {
        'tasks_completed_today': 12,
        'productivity_score': 87,
        'weekly_trend': '+15%',
        'team_performance': 'Above Average',
        'upcoming_deadlines': 3
    }

@app.route('/')
def dashboard():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session['profile'] = {}
    
    apply_config_overrides()
    
    user_id = session['user_id']
    user_tasks = todos_storage.get(user_id, [])
    analytics = generate_analytics_data()
    
    template_data = {
        'user_tasks': user_tasks[:5],
        'recent_tasks': user_tasks,
        'analytics': analytics,
        'app_config': app_config,
        'session_info': {k: v for k, v in session.items() if k != 'profile'},
        'flag_data': FLAG if app_config.admin_access else None
    }
    
    return render_template('dashboard.html', **template_data)

@app.route('/tasks')
def tasks():
    apply_config_overrides()
    user_id = session.get('user_id')
    user_tasks = todos_storage.get(user_id, [])
    
    template_data = {
        'user_tasks': user_tasks,
        'app_config': app_config,
        'session_info': {k: v for k, v in session.items() if k != 'profile'},
        'flag_data': FLAG if app_config.admin_access else None
    }
    
    return render_template('tasks.html', **template_data)

@app.route('/analytics')
def analytics():
    apply_config_overrides()
    analytics_data = generate_analytics_data()
    
    template_data = {
        'analytics': analytics_data,
        'app_config': app_config,
        'session_info': {k: v for k, v in session.items() if k != 'profile'},
        'flag_data': FLAG if app_config.admin_access else None
    }
    
    return render_template('analytics.html', **template_data)

@app.route('/teams')
def teams():
    apply_config_overrides()
    template_data = {
        'app_config': app_config,
        'session_info': {k: v for k, v in session.items() if k != 'profile'},
        'flag_data': FLAG if app_config.admin_access else None
    }
    
    return render_template('teams.html', **template_data)

@app.route('/settings')
def settings():
    apply_config_overrides()
    
    template_data = {
        'app_config': app_config,
        'current_profile': session.get('profile', {}),
        'session_info': {k: v for k, v in session.items() if k != 'profile'},
        'flag_data': FLAG if app_config.admin_access else None
    }
    
    return render_template('settings.html', **template_data)

@app.route('/admin')
def admin_panel():
    apply_config_overrides()
    
    if not app_config.admin_access:
        flash('Access denied. Administrative privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    template_data = {
        'app_config': app_config,
        'session_info': {k: v for k, v in session.items() if k != 'profile'},
        'flag_data': FLAG
    }
    
    return render_template('admin.html', **template_data)

@app.route('/create_task', methods=['POST'])
def create_task():
    if 'user_id' not in session:
        return jsonify({'error': 'Session required'}), 401
    
    user_id = session['user_id']
    
    new_task = {
        'id': str(uuid.uuid4()),
        'title': request.form.get('title', ''),
        'description': request.form.get('description', ''),
        'priority': request.form.get('priority', 'Medium'),
        'category': request.form.get('category', ''),
        'completed': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    if user_id not in todos_storage:
        todos_storage[user_id] = []
    
    todos_storage[user_id].append(new_task)
    flash('Task created successfully!', 'success')
    
    return redirect(url_for('tasks'))

@app.route('/complete_task', methods=['POST'])
def complete_task():
    if 'user_id' not in session:
        return jsonify({'error': 'Session required'}), 401
    
    user_id = session['user_id']
    task_id = request.form.get('task_id')
    
    if user_id in todos_storage:
        for task in todos_storage[user_id]:
            if task['id'] == task_id:
                task['completed'] = True
                flash('Task completed!', 'success')
                break
    
    return redirect(url_for('tasks'))

@app.route('/update_settings', methods=['POST'])
def update_settings():
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    section = request.form.get('section', 'general')
    
    if section == 'general':
        profile = session.get('profile', {})
        profile['display_name'] = request.form.get('display_name', '')
        profile['email'] = request.form.get('email', '')
        session['profile'] = profile
        flash('General settings updated successfully!', 'success')
    
    return redirect(url_for('settings'))

@app.route('/update_profile', methods=['POST'])
def update_user_profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        profile_json = request.form.get('profile_data', '{}')
        new_profile_data = json.loads(profile_json)
        
        current_profile = session.get('profile', {})
        updated_profile = merge_user_preferences(current_profile, new_profile_data)
        session['profile'] = updated_profile
        
        config_keys = ['debug_mode', 'admin_access', 'maintenance_mode', 'feature_flags']
        config_overrides = {}
        
        def extract_config_values(data, prefix=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    full_key = f"{prefix}.{key}" if prefix else key
                    if key in config_keys or any(k in key for k in ['admin', 'debug', 'maintenance']):
                        config_overrides[key] = value
                    if isinstance(value, dict):
                        extract_config_values(value, full_key)
        
        extract_config_values(new_profile_data)
        
        if config_overrides:
            session['config_overrides'] = config_overrides
        
        return redirect(url_for('dashboard') + '?success=Profile updated successfully!')
        
    except json.JSONDecodeError:
        return redirect(url_for('dashboard') + '?error=Invalid JSON format in profile data')
    except Exception as e:
        return redirect(url_for('dashboard') + f'?error=Profile update failed: {str(e)}')

@app.route('/api/system/status')
def system_status():
    apply_config_overrides()
    return jsonify({
        'status': 'operational',
        'version': '3.2.1',
        'debug_mode': app_config.debug_mode,
        'admin_access': app_config.admin_access,
        'maintenance_mode': app_config.maintenance_mode,
        'feature_flags': app_config.feature_flags,
        'session_config': session.get('config_overrides', {}),
        'user_profile': session.get('profile', {})
    })

@app.route('/api/admin/flag')
def admin_flag_endpoint():
    apply_config_overrides()
    if app_config.admin_access:
        return jsonify({
            'flag': FLAG,
            'message': 'Administrative access confirmed - flag retrieved successfully',
            'challenge_name': 'taskflow',
            'difficulty': 'middle'
        })
    else:
        return jsonify({'error': 'Administrative privileges required'}), 403

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy', 
        'service': 'taskflow-pro',
        'version': '3.2.1',
        'uptime': 'operational'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
