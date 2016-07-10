
import os
import pytest
import tempfile

import app
import app.models as models

@pytest.fixture(scope='function')
def ws(request):
    flask_app = app.app.app
    # Yuck!  Reeeally have to fix the app name!

    fd, fn = tempfile.mkstemp()
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + fn
    flask_app.config['TESTING'] = True
    inst = flask_app.test_client()
    with flask_app.app_context():
        app.models.db.create_all()
        pass

    def fin():
        os.close(fd)
        os.unlink(fn)
    request.addfinalizer(fin)
    return inst


@pytest.fixture(scope='function')
def sample(ws):
    models.add_project(name='Manhattan', sample_mask='man-###')
    models.add_sample(project_id='PqrX9', name='sample 1')
    models.add_method(name='X-ray tomography', description='Placeholder description.')
