from flask import request, jsonify, Blueprint
import services.ranking_service as logic

ranking_bp = Blueprint("ranking", __name__, url_prefix="/ranking")

@ranking_bp.route("/", methods=["GET"])
def obtener_ranking():
    limit = request.args.get('_limit', default=10, type=int)
    offset = request.args.get('_offset', default=0, type=int)

    ranking, total = logic.obtener_ranking(limit, offset)

    response = {
        "ranking": ranking if ranking else [],
        "total": total
    }

    return jsonify(response), 200