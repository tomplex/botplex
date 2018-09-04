
from flask import render_template, request
from flask.json import jsonify


from app import nugs_manager, archive_manager, app
from app.database import Database
from app.background_task import run_background_task


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/refresh_nugs_items', methods=['POST'])
def refresh_nugs_items():
    run_background_task(nugs_manager.run_full_metadata_update)
    return jsonify({'success': True, 'error': None})


@app.route('/refresh_all_archive_items', methods=['POST'])
def refresh_archive_items():
    run_background_task(archive_manager.run_metadata_update)
    return jsonify({'success': True, 'error': None})


@app.route('/refresh_new_archive_items', methods=['POST'])
def partial_refresh_archive_items():
    run_background_task(lambda: archive_manager.run_metadata_update(update_type='partial'))
    return jsonify({'success': True, 'error': None})


@app.route('/metadata_status', methods=['GET'])
def metadata_status():
    with Database() as db:
        # nugs = db.query('SELECT row_to_json(r) FROM (select * from nugs_metadata) r')
        # archive = db.query('SELECT row_to_json(r) FROM (select * from archive_metadata) r')
        nugs = db.query('SELECT * FROM nugs_metadata')
        archive = db.query('select * from archive_metadata')
        sql = """
        SELECT json_build_object('nugs', row_to_json(
        
        """

    data = {
        'nugs': {
            'last_refresh_date': nugs[0],
            'refresh_in_progress': bool(nugs[1])
        },
        'archive': {
            'last_refresh_date': archive[0],
            'last_partial_refresh_date': archive[1],
            'refresh_in_progress': bool(archive[2])
        }
    }

    return jsonify(data)


@app.route('/replies', methods=['GET'])
def replies():
    with Database() as db:
        limit = request.args.get('limit', 'ALL')
        sql = f"""
        SELECT json_agg(row_to_json(r)) FROM (SELECT * FROM replies ORDER BY reply_date DESC LIMIT {limit}) r
        """
        results = db.query(sql)

    return jsonify(results)
