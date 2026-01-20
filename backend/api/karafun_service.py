"""
Karafun Business API Service
Integrates with Karafun Business API for karaoke device management
"""

import requests
from django.conf import settings


class KarafunAPI:
    """Client for Karafun Business API"""
    
    def __init__(self, api_token=None, api_url=None):
        self.api_token = api_token or settings.KARAFUN_API_TOKEN
        self.api_url = api_url or settings.KARAFUN_API_URL
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, method, endpoint, data=None):
        """Make HTTP request to Karafun API"""
        url = f"{self.api_url}{endpoint}"
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                timeout=10
            )
            response.raise_for_status()
            return {
                'success': True,
                'data': response.json() if response.content else {}
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }
    
    def list_devices(self):
        """List all Karafun devices"""
        return self._make_request('GET', '/device/list')
    
    def get_sessions(self, start_at_timestamp=None, end_at_timestamp=None):
        """Get sessions between two dates (ISO 8601 format with timezone)"""
        endpoint = '/session/'
        params = []
        if start_at_timestamp:
            params.append(f'start_at_timestamp={start_at_timestamp}')
        if end_at_timestamp:
            params.append(f'end_at_timestamp={end_at_timestamp}')
        if params:
            endpoint += '?' + '&'.join(params)
        return self._make_request('GET', endpoint)
    
    def create_session(self, device_id, start_at_timestamp, end_at_timestamp, 
                      locale='en', customer_firstname=None, comment=None):
        """Create a new karaoke session on a device"""
        data = {
            'device_id': device_id,
            'start_at_timestamp': start_at_timestamp,
            'end_at_timestamp': end_at_timestamp,
            'locale': locale
        }
        if customer_firstname:
            data['customer_firstname'] = customer_firstname
        if comment:
            data['comment'] = comment
        return self._make_request('POST', '/session/', data=data)
    
    def get_session_info(self, session_id):
        """Get details about a specific session"""
        return self._make_request('GET', f'/session/{session_id}/')
    
    def edit_session(self, session_id, **kwargs):
        """Edit an existing session"""
        return self._make_request('PATCH', f'/session/{session_id}/', data=kwargs)
    
    def delete_session(self, session_id):
        """Delete a session"""
        return self._make_request('DELETE', f'/session/{session_id}/')
    
    def edit_device(self, device_id, name=None, parental_control=None, show_quiz=None):
        """Edit a device configuration"""
        data = {}
        if name is not None:
            data['name'] = name
        if parental_control is not None:
            data['parental_control'] = parental_control
        if show_quiz is not None:
            data['show_quiz'] = show_quiz
        return self._make_request('PATCH', f'/device/{device_id}/', data=data)
