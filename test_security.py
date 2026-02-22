"""
Security tests for input validation and sanitization
"""
import sys
sys.path.insert(0, '.')

from app import validate_text_input, sanitize_input, MAX_TEXT_LENGTH


def test_text_length_validation():
    """Test that text length is properly validated"""
    print("Testing text length validation...")
    
    # Valid length
    valid_text = "a" * 1000
    is_valid, error = validate_text_input(valid_text)
    assert is_valid, "Valid length text should pass"
    
    # Exactly at max length
    max_text = "a" * MAX_TEXT_LENGTH
    is_valid, error = validate_text_input(max_text)
    assert is_valid, "Text at max length should pass"
    
    # Over max length
    over_text = "a" * (MAX_TEXT_LENGTH + 1)
    is_valid, error = validate_text_input(over_text)
    assert not is_valid, "Text over max length should fail"
    assert "exceeds maximum length" in error
    
    print("✅ Text length validation passed")


def test_empty_text_validation():
    """Test that empty text is rejected"""
    print("Testing empty text validation...")
    
    # Empty string
    is_valid, error = validate_text_input("")
    assert not is_valid, "Empty string should fail"
    
    # Whitespace only
    is_valid, error = validate_text_input("   \n\t  ")
    assert not is_valid, "Whitespace-only text should fail"
    
    # Valid text with whitespace
    is_valid, error = validate_text_input("  Valid text  ")
    assert is_valid, "Valid text with whitespace should pass"
    
    print("✅ Empty text validation passed")


def test_injection_pattern_detection():
    """Test that suspicious injection patterns are detected"""
    print("Testing injection pattern detection...")
    
    # Excessive HTML brackets
    is_valid, error = validate_text_input("<" * 60)
    assert not is_valid, "Excessive < should fail"
    assert "HTML-like brackets" in error
    
    # Excessive curly braces
    is_valid, error = validate_text_input("{" * 60)
    assert not is_valid, "Excessive { should fail"
    assert "curly braces" in error
    
    # Excessive square brackets
    is_valid, error = validate_text_input("[" * 60)
    assert not is_valid, "Excessive [ should fail"
    assert "square brackets" in error
    
    # Excessive semicolons
    is_valid, error = validate_text_input(";" * 25)
    assert not is_valid, "Excessive ; should fail"
    assert "semicolons" in error
    
    # Normal use of special characters
    is_valid, error = validate_text_input("Article [source] says <quote> is {important}; more text.")
    assert is_valid, "Normal special character use should pass"
    
    print("✅ Injection pattern detection passed")


def test_html_sanitization():
    """Test that HTML is properly sanitized"""
    print("Testing HTML sanitization...")
    
    # XSS attempt
    xss = '<script>alert("xss")</script>'
    sanitized = sanitize_input(xss)
    assert '<script>' not in sanitized, "Script tags should be escaped"
    assert '&lt;script&gt;' in sanitized, "Script tags should be HTML-escaped"
    
    # HTML entities
    html_text = '<div>Hello & goodbye</div>'
    sanitized = sanitize_input(html_text)
    assert '<div>' not in sanitized, "Div tags should be escaped"
    
    print("✅ HTML sanitization passed")


def test_null_byte_removal():
    """Test that null bytes are removed"""
    print("Testing null byte removal...")
    
    text_with_null = "Hello\x00World"
    sanitized = sanitize_input(text_with_null)
    assert '\x00' not in sanitized, "Null bytes should be removed"
    assert 'HelloWorld' in sanitized, "Text should remain"
    
    print("✅ Null byte removal passed")


def test_unicode_handling():
    """Test that unicode is properly handled"""
    print("Testing unicode handling...")
    
    # Various unicode characters
    unicode_texts = [
        "Café résumé",
        "日本語テキスト",
        "Emoji test 🎉🔥💯",
        "Cyrillic: Привет",
        "Arabic: مرحبا",
    ]
    
    for text in unicode_texts:
        is_valid, error = validate_text_input(text)
        assert is_valid, f"Unicode text should be valid: {text}"
        
        sanitized = sanitize_input(text)
        assert len(sanitized) > 0, f"Sanitized unicode should not be empty: {text}"
    
    print("✅ Unicode handling passed")


def test_special_characters():
    """Test handling of special characters"""
    print("Testing special characters...")
    
    special_texts = [
        "Price: $100.50",
        "Email: test@example.com",
        "Math: 2 + 2 = 4",
        "Quote: \"Hello World\"",
        "Apostrophe: It's working",
        "Percentage: 50% off",
        "Symbols: @#$%^&*()",
    ]
    
    for text in special_texts:
        is_valid, error = validate_text_input(text)
        assert is_valid, f"Special character text should be valid: {text}"
        
        sanitized = sanitize_input(text)
        assert len(sanitized) > 0, f"Sanitized text should not be empty: {text}"
    
    print("✅ Special character handling passed")


def test_newlines_and_whitespace():
    """Test handling of newlines and whitespace"""
    print("Testing newlines and whitespace...")
    
    text_with_newlines = "Paragraph 1.\n\nParagraph 2.\n\nParagraph 3."
    is_valid, error = validate_text_input(text_with_newlines)
    assert is_valid, "Text with newlines should be valid"
    
    sanitized = sanitize_input(text_with_newlines)
    assert '\n' in sanitized, "Newlines should be preserved"
    
    # Tabs
    text_with_tabs = "Column1\tColumn2\tColumn3"
    sanitized = sanitize_input(text_with_tabs)
    assert '\t' in sanitized, "Tabs should be preserved"
    
    print("✅ Newlines and whitespace handling passed")


def test_control_characters():
    """Test that control characters are removed"""
    print("Testing control character removal...")
    
    # Control characters (except newline, tab, carriage return)
    text_with_control = "Hello\x01\x02\x03World"
    sanitized = sanitize_input(text_with_control)
    assert '\x01' not in sanitized, "Control characters should be removed"
    assert 'HelloWorld' in sanitized, "Text should remain"
    
    print("✅ Control character removal passed")


def run_all_tests():
    """Run all security tests"""
    print("=" * 60)
    print("Running Security Tests")
    print("=" * 60)
    
    test_text_length_validation()
    test_empty_text_validation()
    test_injection_pattern_detection()
    test_html_sanitization()
    test_null_byte_removal()
    test_unicode_handling()
    test_special_characters()
    test_newlines_and_whitespace()
    test_control_characters()
    
    print("=" * 60)
    print("✅ ALL SECURITY TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
