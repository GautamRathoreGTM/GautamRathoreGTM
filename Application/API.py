

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle

from datetime import timedelta


class DDOSValidatorView(APIView):
    throttle_classes = []
    
    # Dummy data for demonstration purposes
    dummy_data = [
        {'id': 1, 'ip': '192.168.0.1'},
        {'id': 2, 'ip': '192.168.0.2'},
        {'id': 3, 'ip': '192.168.0.3'},
       
    ]
    def post(self, request):
        return Response(self.dummy_data, status=status.HTTP_200_OK)
    


# bearer_auth_api/api/views.py


class BearerAuthThrottle(UserRateThrottle):
    THROTTLE_BLOCK_TIME = timedelta(minutes=20)
    PERMANENT_BLOCK_THRESHOLD = 100

    def allow_request(self, request, view):
        if request.headers.get('Authorization') == 'Bearer mf8nrqICaHYD1y8wRMBksWm7U7gLgXy1mSWjhI0q':
            # Count the number of requests made by the user within the throttle time window
            self.key = self.get_cache_key(request, view)
            self.history = self.cache.get(self.key, [])
            self.now = self.timer()
            self.history.append(self.now)
            self.history = [
                timestamp for timestamp in self.history
                if timestamp > self.now - self.duration
            ]
            self.cache.set(self.key, self.history, self.duration)
            
            # Check if the user has exceeded the allowed number of requests
            if len(self.history) > 10:
                # Check if the user was previously blocked
                blocked_time = self.cache.get(f'{self.key}_blocked_time')
                if blocked_time and blocked_time > self.now - self.THROTTLE_BLOCK_TIME:
                    return False
                else:
                    # Block the user for the specified time
                    if len(self.history) > self.PERMANENT_BLOCK_THRESHOLD:
                        return False
                    else:
                        self.cache.set(f'{self.key}_blocked_time', self.now, self.THROTTLE_BLOCK_TIME)
                        return False
        return True

class BearerAuthView(APIView):
    throttle_classes = [BearerAuthThrottle]
    throttle_scope = 'user'

    def post(self, request):
        bearer_key = request.headers.get('Authorization')

        if bearer_key != 'Bearer mf8nrqICaHYD1y8wRMBksWm7U7gLgXy1mSWjhI0q':
            return Response({'error': 'Invalid bearer key'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Authentication successful'}, status=status.HTTP_200_OK)


