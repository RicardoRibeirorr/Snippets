<?php
/**
 * Function to sanitize a text string.
 * - Removes all special characters (keeping only letters, numbers, and spaces).
 * - Converts spaces to underscores.
 * - Converts the text to lowercase (optional but common in slugs).
 *
 * @param string $text The input text to sanitize.
 * @return string The sanitized text.
 */
function sanitizeText($text) {
    // Remove all characters that are not letters, numbers, or spaces
    $sanitizedText = preg_replace('/[^a-zA-Z0-9\s]/', '', $text);

    // Replace all spaces with underscores
    $sanitizedText = str_replace(' ', '_', $sanitizedText);

    // Convert to lowercase (optional)
    $sanitizedText = strtolower($sanitizedText);

    return $sanitizedText;
}

// Example usage:
$inputTitle = "Hello World! This is a Test.";
$sanitizedTitle = sanitizeText($inputTitle);
echo $sanitizedTitle; // Output: hello_world_this_is_a_test
?>
