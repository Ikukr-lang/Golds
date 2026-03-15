from flask import Blueprint, render_template
from models import Tournament

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    return render_template('index.html')

@public_bp.route('/league/<int:t_id>')
def league(t_id):
    tour = Tournament.query.get_or_404(t_id)
    # те же расчёты таблицы
    standings = []
    for team in tour.teams:
        points = 0
        for m in tour.matches:
            if m.home_team_id == team.id:
                if m.home_goals > m.away_goals: points += 3
                elif m.home_goals == m.away_goals: points += 1
            elif m.away_team_id == team.id:
                if m.away_goals > m.home_goals: points += 3
                elif m.away_goals == m.home_goals: points += 1
        standings.append({'name': team.name, 'points': points})
    standings.sort(key=lambda x: x['points'], reverse=True)
    
    return render_template('public_league.html', tournament=tour, standings=standings)
