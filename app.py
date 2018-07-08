import os.path as osp
import os
import time
from git import Repo
from flask import Flask
from flask import jsonify, url_for
from celery import Celery

join = osp.join
app = Flask(__name__)
redis_host = os.getenv('redis_host', 'localhost')
app.config['CELERY_BROKER_URL'] = 'redis://{0}:6379/0'.format(redis_host)
app.config['CELERY_RESULT_BACKEND'] = 'redis://{0}:6379/0'.format(redis_host)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task(bind=True)
def repo_pull_task(self):
    repo = Repo.init(join(os.getenv('repo_path', '/home/deepblack/projects/git_repo_sample')))
    self.update_state(state='PROGRESS',
                      meta={'current': '10', 'total': '100', 'status': 'in progress',
                            'latest_commit': str(repo.head.commit.hexsha)
                            }
                      )
    time.sleep(10)

    remote = repo.remotes.origin
    self.update_state(state='PROGRESS',
                      meta={'current': '30', 'total': '100', 'status': 'in progress',
                            'latest_commit': str(repo.head.commit.hexsha)
                            }
                      )
    time.sleep(10)

    remote.pull()
    self.update_state(state='PROGRESS',
                      meta={'current': '80', 'total': '100', 'status': 'in progress',
                            'latest_commit': str(repo.head.commit.hexsha)
                            }
                      )
    time.sleep(10)
    return {'current': 100, 'total': 100, 'status': 'completed', 'latest_commit': str(repo.head.commit.hexsha)}


def get_repository_info(repo):
    return {'repo_description': repo.description,
            'remote': [remote.url for remote in repo.remotes],
            'latest_commit': str(repo.head.commit.hexsha),
            'active_branch': str(repo.active_branch),
            'pull_url': url_for('repo_pull')
            }


@app.route("/")
def repo_info():
    repo = Repo.init(join(os.getenv('repo_path', '/home/deepblack/projects/git_repo_sample')))
    return jsonify(get_repository_info(repo))


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = repo_pull_task.AsyncResult(task_id)
    response = {
        'state': task.state,
        'status': str(task.info),  # this is the exception raised
    }
    return jsonify(response)


@app.route("/pull")
def repo_pull():
    task = repo_pull_task.apply_async()
    return jsonify({'status': 'accepted', 'task_id': task.id, 'result_url': url_for('taskstatus', task_id=task.id)})
