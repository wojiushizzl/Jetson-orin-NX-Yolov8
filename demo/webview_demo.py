import webview

if __name__ == '__main__':
    # Create a standard webview window
    webview.create_window(
        'Confirm Quit Example', 'webview.html', confirm_close=True
    )
    webview.start()