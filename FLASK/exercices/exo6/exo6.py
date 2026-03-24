# ## Exercice 6: Blog Simple (CRUD Complet)

# **Énoncé**:
# Créez une API blog complète avec:
# - `GET /posts` - Lister tous les articles
# - `GET /posts/<id>` - Détail d'un article
# - `POST /posts` - Créer un article
# - `PUT /posts/<id>` - Modifier un article
# - `DELETE /posts/<id>` - Supprimer un article

# Structure d'un post:
# ```json
# {
#   "id": 1,
#   "title": "Mon Premier Article",
#   "content": "Contenu...",
#   "author": "John",
#   "created_at": "2024-01-01T10:00:00",
#   "updated_at": "2024-01-01T10:00:00"
# }


from flask import Blueprint, jsonify, request
from .post_store import (
    list_posts,
    get_post_by_id,
    create_post as create_post_service,
    update_post as update_post_service,
    delete_post as delete_post_service,
)

bp = Blueprint('posts', __name__)



@bp.route('/posts', methods=['GET'])
def get_posts():

    return jsonify(list_posts()), 200


@bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):

    post = get_post_by_id(post_id)
    if not post:
        return jsonify({'error': f'Post with ID {post_id} not found'}), 404
    return jsonify(post), 200


@bp.route('/posts', methods=['POST'])
def create_post():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400

        result, status = create_post_service(data)

        return jsonify(result), status
    except Exception as e:

        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400

        result, status = update_post_service(post_id, data)

        return jsonify(result), status
    except Exception as e:

        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        result, status = delete_post_service(post_id)

        return jsonify(result), status
    except Exception as e:

        return jsonify({'error': 'Internal server error'}), 500
