#!/usr/bin/env python3
"""
Accessibility Guidelines Exercise
Python implementation demonstrating accessibility testing and compliance checking
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import requests
from urllib.parse import urljoin, urlparse
import colorsys


class WCAGLevel(Enum):
    """WCAG Compliance Levels"""
    A = "A"
    AA = "AA"
    AAA = "AAA"


class IssueType(Enum):
    """Types of accessibility issues"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class AccessibilityIssue:
    """Represents an accessibility issue found during testing"""
    issue_type: IssueType
    wcag_level: WCAGLevel
    description: str
    element: str
    recommendation: str
    wcag_criteria: str


class ColorContrastChecker:
    """Checks color contrast compliance with WCAG guidelines"""

    def __init__(self):
        self.wcag_aa_normal = 4.5
        self.wcag_aa_large = 3.0
        self.wcag_aaa_normal = 7.0
        self.wcag_aaa_large = 4.5

    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB values"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def get_relative_luminance(self, rgb: Tuple[int, int, int]) -> float:
        """Calculate relative luminance according to WCAG formula"""

        def get_linear_rgb(value):
            value = value / 255.0
            if value <= 0.03928:
                return value / 12.92
            else:
                return pow((value + 0.055) / 1.055, 2.4)

        r, g, b = rgb
        r_linear = get_linear_rgb(r)
        g_linear = get_linear_rgb(g)
        b_linear = get_linear_rgb(b)

        return 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear

    def calculate_contrast_ratio(self, color1: str, color2: str) -> float:
        """Calculate contrast ratio between two colors"""
        rgb1 = self.hex_to_rgb(color1)
        rgb2 = self.hex_to_rgb(color2)

        lum1 = self.get_relative_luminance(rgb1)
        lum2 = self.get_relative_luminance(rgb2)

        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)

        return (lighter + 0.05) / (darker + 0.05)

    def check_contrast_compliance(self, foreground: str, background: str,
                                  is_large_text: bool = False) -> Dict:
        """Check if color combination meets WCAG contrast requirements"""
        ratio = self.calculate_contrast_ratio(foreground, background)

        aa_threshold = self.wcag_aa_large if is_large_text else self.wcag_aa_normal
        aaa_threshold = self.wcag_aaa_large if is_large_text else self.wcag_aaa_normal

        return {
            'contrast_ratio': round(ratio, 2),
            'wcag_aa_pass': ratio >= aa_threshold,
            'wcag_aaa_pass': ratio >= aaa_threshold,
            'aa_threshold': aa_threshold,
            'aaa_threshold': aaa_threshold,
            'is_large_text': is_large_text
        }


class HTMLAccessibilityChecker:
    """Checks HTML content for accessibility compliance"""

    def __init__(self):
        self.issues = []
        self.color_checker = ColorContrastChecker()

    def check_images(self, html_content: str) -> List[AccessibilityIssue]:
        """Check for image accessibility issues"""
        issues = []

        # Find all img tags
        img_pattern = r'<img[^>]*>'
        images = re.findall(img_pattern, html_content, re.IGNORECASE)

        for img in images:
            # Check for missing alt attribute
            if 'alt=' not in img.lower():
                issues.append(AccessibilityIssue(
                    issue_type=IssueType.ERROR,
                    wcag_level=WCAGLevel.A,
                    description="Image missing alt attribute",
                    element=img,
                    recommendation="Add descriptive alt text or alt='' for decorative images",
                    wcag_criteria="1.1.1 Non-text Content"
                ))

            # Check for suspicious alt text
            alt_match = re.search(r'alt=["\']([^"\']*)["\']', img, re.IGNORECASE)
            if alt_match:
                alt_text = alt_match.group(1).lower()
                suspicious_words = ['image', 'picture', 'photo', 'graphic', 'img']
                if any(word in alt_text for word in suspicious_words):
                    issues.append(AccessibilityIssue(
                        issue_type=IssueType.WARNING,
                        wcag_level=WCAGLevel.A,
                        description="Suspicious alt text detected",
                        element=img,
                        recommendation="Use descriptive alt text that conveys the image's purpose",
                        wcag_criteria="1.1.1 Non-text Content"
                    ))

        return issues

    def check_headings(self, html_content: str) -> List[AccessibilityIssue]:
        """Check heading structure for accessibility"""
        issues = []

        # Find all heading tags
        heading_pattern = r'<h([1-6])[^>]*>(.*?)</h[1-6]>'
        headings = re.findall(heading_pattern, html_content, re.IGNORECASE | re.DOTALL)

        if not headings:
            issues.append(AccessibilityIssue(
                issue_type=IssueType.WARNING,
                wcag_level=WCAGLevel.AA,
                description="No headings found",
                element="document",
                recommendation="Use headings to structure content hierarchically",
                wcag_criteria="2.4.6 Headings and Labels"
            ))
            return issues

        # Check if first heading is H1
        if headings and int(headings[0][0]) != 1:
            issues.append(AccessibilityIssue(
                issue_type=IssueType.WARNING,
                wcag_level=WCAGLevel.AA,
                description="Page doesn't start with H1",
                element=f"<h{headings[0][0]}>{headings[0][1][:50]}...</h{headings[0][0]}>",
                recommendation="Start page with H1 heading",
                wcag_criteria="2.4.6 Headings and Labels"
            ))

        # Check for heading sequence violations
        for i in range(1, len(headings)):
            current_level = int(headings[i][0])
            previous_level = int(headings[i - 1][0])

            if current_level > previous_level + 1:
                issues.append(AccessibilityIssue(
                    issue_type=IssueType.WARNING,
                    wcag_level=WCAGLevel.AA,
                    description="Heading level skipped",
                    element=f"<h{current_level}>{headings[i][1][:50]}...</h{current_level}>",
                    recommendation="Don't skip heading levels (e.g., H1 to H3)",
                    wcag_criteria="2.4.6 Headings and Labels"
                ))

        return issues

    def check_forms(self, html_content: str) -> List[AccessibilityIssue]:
        """Check form accessibility"""
        issues = []

        # Find input elements
        input_pattern = r'<input[^>]*>'
        inputs = re.findall(input_pattern, html_content, re.IGNORECASE)

        for input_elem in inputs:
            # Skip hidden inputs and buttons
            if 'type="hidden"' in input_elem.lower() or 'type="submit"' in input_elem.lower():
                continue

            # Check for missing labels
            id_match = re.search(r'id=["\']([^"\']*)["\']', input_elem, re.IGNORECASE)
            if id_match:
                input_id = id_match.group(1)
                label_pattern = f'<label[^>]*for=["\']?{input_id}["\']?[^>]*>'
                if not re.search(label_pattern, html_content, re.IGNORECASE):
                    issues.append(AccessibilityIssue(
                        issue_type=IssueType.ERROR,
                        wcag_level=WCAGLevel.A,
                        description="Form input missing associated label",
                        element=input_elem,
                        recommendation="Add <label for='input_id'> or aria-label attribute",
                        wcag_criteria="3.3.2 Labels or Instructions"
                    ))
            else:
                # No ID found, check for aria-label
                if 'aria-label' not in input_elem.lower():
                    issues.append(AccessibilityIssue(
                        issue_type=IssueType.ERROR,
                        wcag_level=WCAGLevel.A,
                        description="Form input has no ID or aria-label",
                        element=input_elem,
                        recommendation="Add id attribute and corresponding label, or aria-label",
                        wcag_criteria="3.3.2 Labels or Instructions"
                    ))

        return issues

    def check_links(self, html_content: str) -> List[AccessibilityIssue]:
        """Check link accessibility"""
        issues = []

        # Find all links
        link_pattern = r'<a[^>]*>(.*?)</a>'
        links = re.findall(link_pattern, html_content, re.IGNORECASE | re.DOTALL)

        for link_text in links:
            # Remove HTML tags from link text
            clean_text = re.sub(r'<[^>]+>', '', link_text).strip()

            # Check for empty links
            if not clean_text:
                issues.append(AccessibilityIssue(
                    issue_type=IssueType.ERROR,
                    wcag_level=WCAGLevel.A,
                    description="Empty link text",
                    element=f"<a>{link_text}</a>",
                    recommendation="Provide descriptive link text or aria-label",
                    wcag_criteria="2.4.4 Link Purpose"
                ))

            # Check for non-descriptive link text
            generic_text = ['click here', 'read more', 'more', 'link', 'here']
            if clean_text.lower() in generic_text:
                issues.append(AccessibilityIssue(
                    issue_type=IssueType.WARNING,
                    wcag_level=WCAGLevel.AA,
                    description="Non-descriptive link text",
                    element=f"<a>{link_text}</a>",
                    recommendation="Use descriptive link text that explains the destination",
                    wcag_criteria="2.4.4 Link Purpose"
                ))

        return issues

    def analyze_html(self, html_content: str) -> List[AccessibilityIssue]:
        """Perform comprehensive accessibility analysis of HTML content"""
        all_issues = []

        all_issues.extend(self.check_images(html_content))
        all_issues.extend(self.check_headings(html_content))
        all_issues.extend(self.check_forms(html_content))
        all_issues.extend(self.check_links(html_content))

        return all_issues


class AccessibilityReporter:
    """Generates accessibility reports"""

    def __init__(self):
        pass

    def generate_summary(self, issues: List[AccessibilityIssue]) -> Dict:
        """Generate summary statistics from issues"""
        summary = {
            'total_issues': len(issues),
            'errors': len([i for i in issues if i.issue_type == IssueType.ERROR]),
            'warnings': len([i for i in issues if i.issue_type == IssueType.WARNING]),
            'info': len([i for i in issues if i.issue_type == IssueType.INFO]),
            'wcag_level_breakdown': {
                'A': len([i for i in issues if i.wcag_level == WCAGLevel.A]),
                'AA': len([i for i in issues if i.wcag_level == WCAGLevel.AA]),
                'AAA': len([i for i in issues if i.wcag_level == WCAGLevel.AAA])
            }
        }
        return summary

    def generate_detailed_report(self, issues: List[AccessibilityIssue]) -> str:
        """Generate detailed text report"""
        report = "ACCESSIBILITY ANALYSIS REPORT\n"
        report += "=" * 50 + "\n\n"

        summary = self.generate_summary(issues)

        report += f"SUMMARY:\n"
        report += f"Total Issues: {summary['total_issues']}\n"
        report += f"Errors: {summary['errors']}\n"
        report += f"Warnings: {summary['warnings']}\n"
        report += f"Info: {summary['info']}\n\n"

        report += f"WCAG Level Breakdown:\n"
        report += f"Level A: {summary['wcag_level_breakdown']['A']}\n"
        report += f"Level AA: {summary['wcag_level_breakdown']['AA']}\n"
        report += f"Level AAA: {summary['wcag_level_breakdown']['AAA']}\n\n"

        # Group issues by type
        errors = [i for i in issues if i.issue_type == IssueType.ERROR]
        warnings = [i for i in issues if i.issue_type == IssueType.WARNING]

        if errors:
            report += "ERRORS (Must Fix):\n"
            report += "-" * 20 + "\n"
            for i, issue in enumerate(errors, 1):
                report += f"{i}. {issue.description}\n"
                report += f"   WCAG: {issue.wcag_criteria} (Level {issue.wcag_level.value})\n"
                report += f"   Element: {issue.element[:100]}...\n"
                report += f"   Fix: {issue.recommendation}\n\n"

        if warnings:
            report += "WARNINGS (Should Fix):\n"
            report += "-" * 22 + "\n"
            for i, issue in enumerate(warnings, 1):
                report += f"{i}. {issue.description}\n"
                report += f"   WCAG: {issue.wcag_criteria} (Level {issue.wcag_level.value})\n"
                report += f"   Element: {issue.element[:100]}...\n"
                report += f"   Fix: {issue.recommendation}\n\n"

        return report


def demonstrate_color_contrast():
    """Demonstrate color contrast checking"""
    print("COLOR CONTRAST DEMONSTRATION")
    print("=" * 40)

    checker = ColorContrastChecker()

    # Test different color combinations
    test_combinations = [
        ("#000000", "#FFFFFF", False, "Black on White (normal text)"),
        ("#FFFFFF", "#000000", False, "White on Black (normal text)"),
        ("#666666", "#FFFFFF", False, "Gray on White (normal text)"),
        ("#0066CC", "#FFFFFF", False, "Blue on White (normal text)"),
        ("#FF0000", "#FFFFFF", True, "Red on White (large text)"),
        ("#999999", "#CCCCCC", False, "Light Gray on Lighter Gray (poor contrast)"),
    ]

    for fg, bg, is_large, description in test_combinations:
        result = checker.check_contrast_compliance(fg, bg, is_large)

        print(f"\n{description}")
        print(f"Foreground: {fg}, Background: {bg}")
        print(f"Contrast Ratio: {result['contrast_ratio']}:1")
        print(f"WCAG AA: {'PASS' if result['wcag_aa_pass'] else 'FAIL'} (needs {result['aa_threshold']}:1)")
        print(f"WCAG AAA: {'PASS' if result['wcag_aaa_pass'] else 'FAIL'} (needs {result['aaa_threshold']}:1)")


def test_sample_html():
    """Test accessibility checker with sample HTML"""
    print("\nHTML ACCESSIBILITY ANALYSIS")
    print("=" * 40)

    # Sample HTML with various accessibility issues
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sample Page</title>
    </head>
    <body>
        <h2>Welcome to Our Site</h2>
        <img src="logo.png" width="200">
        <img src="decorative.jpg" alt="image of our building">

        <h1>Main Content</h1>
        <p>This is some content.</p>

        <h4>Contact Form</h4>
        <form>
            <input type="text" placeholder="Enter your name">
            <label for="email">Email:</label>
            <input type="email" id="email">
            <input type="submit" value="Submit">
        </form>

        <p><a href="about.html">Click here</a> for more information.</p>
        <p><a href="contact.html">Contact Us</a> to get in touch.</p>
        <p><a href=""></a></p>

        <img src="chart.png" alt="Sales increased 25% in Q3 2024">
    </body>
    </html>
    """

    checker = HTMLAccessibilityChecker()
    issues = checker.analyze_html(sample_html)

    reporter = AccessibilityReporter()
    report = reporter.generate_detailed_report(issues)

    print(report)


def main():
    """Main function to run accessibility guidelines exercise"""
    print("ACCESSIBILITY GUIDELINES EXERCISE")
    print("=" * 50)
    print("This program demonstrates accessibility testing concepts")
    print("and WCAG compliance checking.\n")

    # Demonstrate color contrast checking
    demonstrate_color_contrast()

    # Test HTML accessibility analysis
    test_sample_html()

    # Interactive mode
    while True:
        print("\n" + "=" * 50)
        print("INTERACTIVE MODE")
        print("1. Test color contrast")
        print("2. Analyze HTML snippet")
        print("3. Exit")

        choice = input("\nSelect an option (1-3): ").strip()

        if choice == "1":
            try:
                fg = input("Enter foreground color (hex, e.g., #000000): ").strip()
                bg = input("Enter background color (hex, e.g., #FFFFFF): ").strip()
                large = input("Is this large text? (y/n): ").strip().lower() == 'y'

                checker = ColorContrastChecker()
                result = checker.check_contrast_compliance(fg, bg, large)

                print(f"\nContrast Ratio: {result['contrast_ratio']}:1")
                print(f"WCAG AA: {'PASS' if result['wcag_aa_pass'] else 'FAIL'}")
                print(f"WCAG AAA: {'PASS' if result['wcag_aaa_pass'] else 'FAIL'}")

            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            html = input("Enter HTML snippet to analyze: ").strip()
            if html:
                checker = HTMLAccessibilityChecker()
                issues = checker.analyze_html(html)

                reporter = AccessibilityReporter()
                summary = reporter.generate_summary(issues)

                print(f"\nFound {summary['total_issues']} issues:")
                print(f"Errors: {summary['errors']}, Warnings: {summary['warnings']}")

                if issues:
                    print("\nDetailed issues:")
                    for issue in issues[:3]:  # Show first 3 issues
                        print(f"- {issue.description}")
                        print(f"  Fix: {issue.recommendation}")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()