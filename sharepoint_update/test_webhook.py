import requests
import sys

def test_webhook_validation():
    """测试webhook验证端点"""
    # 从命令行获取ngrok URL，或使用默认值
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "https://5231-122-249-141-175.ngrok-free.app"
    
    webhook_url = f"{base_url}/api/notify"
    test_token = "test-validation-token-12345"
    
    print(f"Testing webhook validation at: {webhook_url}")
    print(f"Test validation token: {test_token}")
    
    try:
        # 模拟Microsoft Graph的验证请求
        response = requests.get(
            webhook_url,
            params={"validationToken": test_token},
            timeout=10
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200 and response.text == test_token:
            print("✓ Webhook validation test PASSED")
            return True
        else:
            print("✗ Webhook validation test FAILED")
            return False
            
    except Exception as e:
        print(f"✗ Error testing webhook: {e}")
        return False

def test_webhook_notification():
    """测试webhook通知端点"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "https://5edd-122-249-141-175.ngrok-free.app"
    
    webhook_url = f"{base_url}/api/notify"
    
    # 模拟通知数据
    test_notification = {
        "value": [
            {
                "subscriptionId": "test-subscription-id",
                "changeType": "updated",
                "resource": "/drives/test-drive-id/root",
                "resourceData": {
                    "id": "test-item-id",
                    "@odata.type": "#Microsoft.Graph.DriveItem"
                }
            }
        ]
    }
    
    print(f"\nTesting webhook notification at: {webhook_url}")
    
    try:
        response = requests.post(
            webhook_url,
            json=test_notification,
            timeout=10
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")
        
        if response.status_code in [200, 202]:
            print("✓ Webhook notification test PASSED")
            return True
        else:
            print("✗ Webhook notification test FAILED")
            return False
            
    except Exception as e:
        print(f"✗ Error testing webhook notification: {e}")
        return False

if __name__ == "__main__":
    print("=== Webhook Endpoint Test ===")
    
    # 测试验证端点
    validation_ok = test_webhook_validation()
    
    # 测试通知端点
    notification_ok = test_webhook_notification()
    
    print(f"\n=== Test Results ===")
    print(f"Validation test: {'PASS' if validation_ok else 'FAIL'}")
    print(f"Notification test: {'PASS' if notification_ok else 'FAIL'}")
    
    if validation_ok and notification_ok:
        print("✓ All tests passed! Your webhook should work with Microsoft Graph subscriptions.")
    else:
        print("✗ Some tests failed. Please check your webhook implementation.")
