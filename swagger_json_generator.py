import json
from pprint import pprint

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify
from marshmallow import Schema, fields


class NonStopParameter(Schema):
    gist_id = fields.Int()


class NonStopSchema(Schema):
    id = fields.Int()
    content = fields.Str()


spec = APISpec(
    title="NonStop Hack&Change 2024",
    version="1.0.0",
    openapi_version="3.0.2",
    info=dict(
        description="NonStop Hack&Change 2024 API",
        version="1.0.0-oas3", 
        license=dict(
            name="Apache 2.0",
            url='http://www.apache.org/licenses/LICENSE-2.0.html'
            )
        ),
    tags=[
        dict(
            name="NonStop",
            description="Endpoints related to Demo"
            )
        ],
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

spec.components.schema("NonStop", schema=NonStopSchema)

# spec.components.schema(
#     "Gist",
#     {
#         "properties": {
#             "id": {"type": "integer", "format": "int64"},
#             "name": {"type": "string"},
#         }
#     },
# )
#
# spec.path(
#     path="/gist/{gist_id}",
#     operations=dict(
#         get=dict(
#             responses={"200": {"content": {"application/json": {"schema": "Gist"}}}}
#         )
#     ),
# )
# Extensions initialization
# =========================
app = Flask(__name__)


@app.route("/demo/<gist_id>", methods=["GET"])
def my_route(gist_id):
    """Gist detail view.
    ---
    get:
      parameters:
      - in: path
        schema: NonStopParameter
      responses:
        200:
          content:
            application/json:
              schema: DemoSchema
        201:
          content:
            application/json:
              schema: DemoSchema
    """
    # (...)
    return jsonify('foo')


# Since path inspects the view and its route,
# we need to be in a Flask request context
with app.test_request_context():
    spec.path(view=my_route)
# We're good to go! Save this to a file for now.
with open('swagger.json', 'w') as f:
    json.dump(spec.to_dict(), f)

pprint(spec.to_dict())
print(spec.to_yaml())