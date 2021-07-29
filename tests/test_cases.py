test_scraper_data = [
    # Test Case 1: Single exact word
    {
        "content": "<html>\n<title>Hello, World!</title>\n<body>\n<h1>Goodbye!</h1>\n</body>\n</html>",
        "count": 1,
        "word": "Hello",
    },
    # Test Case 2: Multiple exact words
    {
        "content": "<html>\n<title>Hello, World!</title>\n<body>\n<h1>Goodbye, World!</h1>\n</body>\n</html>",
        "count": 2,
        "word": "World",
    },
    # Test Case 3: Substring words
    {
        "content": "<html>\n<head><title>Hello, World!</title><style>body { margin: 10px; } </style></head><\n<body>\n<h1>in information inside into mint</h1>\n</body>\n</html>",
        "count": 1,
        "word": "in",
    },
    # Test Case 4: No words present
    {
        "content": "<html>\n<title>Hello, World!</title>\n<body>\n<h1>Goodbye, World!</h1>\n</body>\n</html>",
        "count": 0,
        "word": "test",
    },
]

test_invalid_requests_data = [
    # Test Case 1: Request body different from API contract
    {"test": ""},
    # Test Case 2: Empty string for word and url
    {"word": "", "url": ""},
    # Test Case 3: Empty string for word
    {"word": "", "url": "http://example.com"},
    # Test Case 4: Empty string for url
    {"word": "test", "url": ""},
    # Test Case 5: Invalid url
    {"word": "test", "url": "test"},
    # Test Case 6: Invalid word
    {"word": ["test"], "url": "http://example.com"},
]
