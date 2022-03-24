from typing import Optional, Dict, Any
import traceback

from fastapi import status, HTTPException

from .error_messages import ErrorMessage, BaseMessage


class APIException(HTTPException):
    """ API例外
    """
    default_status_code = status.HTTP_400_BAD_REQUEST

    def __init__(
        self,
        error,
        status_code: int = default_status_code,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.status_code = status_code
        self.detail = []
        self.headers = headers
        
        # msg_paramsにセットしたパラメータをtextに展開する
        try:
            message = error['error_code'].text.format(error['msg_param'])
        except:
            message = error['error_code'].text

        self.detail = {
            'error_code': str(error['error_code']),
            'error_msg': message 
        } 
        
        super().__init__(self.status_code, self.detail)
