from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import db, Tournament, Team, Match
from datetime import datetime

tournament_bp = Blueprint('tournament', __name__)

@tournament_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        tour = Tournament(name=name, user_id=current_user.id)
        db.session.add(tour)
        db.session.commit()
        flash('Турнир создан!')
        return redirect(url_for('tournament.detail', t_id=tour.id))
    return render_template('create_tournament.html')

@tournament_bp.route('/<int:t_id>')
@login_required
def detail(t_id):
    tour = Tournament.query.get_or_404(t_id)
    if tour.user_id != current_user.id:
        flash('Нет доступа')
        return redirect(url_for('dashboard.index'))
    
    # Расчёт турнирной таблицы
    standings = []
    for team in tour.teams:
        points = 0
        for match in tour.matches:
            if match.home_team_id == team.id:
                if match.home_goals > match.away_goals: points += 3
                elif match.home_goals == match.away_goals: points += 1
            elif match.away_team_id == team.id:
                if match.away_goals > match.home_goals: points += 3
                elif match.away_goals == match.home_goals: points += 1
        standings.append({'name': team.name, 'points': points})
    
    standings.sort(key=lambda x: x['points'], reverse=True)
    
    return render_template('tournament_detail.html', 
                           tournament=tour, 
                           standings=standings)

@tournament_bp.route('/<int:t_id>/add_team', methods=['POST'])
@login_required
def add_team(t_id):
    tour = Tournament.query.get_or_404(t_id)
    name = request.form.get('team_name')
    team = Team(name=name, tournament_id=t_id)
    db.session.add(team)
    db.session.commit()
    flash('Команда добавлена!')
    return redirect(url_for('tournament.detail', t_id=t_id))

@tournament_bp.route('/<int:t_id>/add_match', methods=['POST'])
@login_required
def add_match(t_id):
    tour = Tournament.query.get_or_404(t_id)
    home_id = int(request.form.get('home_team'))
    away_id = int(request.form.get('away_team'))
    date_str = request.form.get('date')
    date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
    
    match = Match(
        home_team_id=home_id,
        away_team_id=away_id,
        date=date,
        tournament_id=t_id
    )
    db.session.add(match)
    db.session.commit()
    flash('Матч добавлен!')
    return redirect(url_for('tournament.detail', t_id=t_id))
