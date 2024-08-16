from flask import Blueprint, request, jsonify

from .ruc_details_service_factory import RucDetailServiceFactory
from ...shared.domain.api_exception import ApiException

ruc_details = Blueprint('ruc_details', __name__)

ruc_service = RucDetailServiceFactory.create('selenium')


@ruc_details.route('/ruc/<string:ruc>', methods=['GET'])
def get_ruc_details(ruc):
    try:
        ruc_detail = ruc_service.consultar_ruc(ruc)

        return jsonify(ruc_detail.to_dict()), 200
    except ApiException as e:
        return jsonify({"message": str(e)}), e.status_code
    except Exception as e:
        return jsonify({"error": f"Ocurrió un error interno del servidor: {str(e)}"}), 500
