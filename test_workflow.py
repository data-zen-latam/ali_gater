"""Disposable test script for Gater workflow - extract claims and generate questions."""

import asyncio
from src.ali_gater.ali_gater import Gater

# Test URL
TEST_URL = "https://briandoddonleadership.com/2019/06/20/truett-cathys-6-legacy-principles-for-leading-chick-fil-a/"


async def test_full_workflow():
    """Test the complete Gater workflow: load -> extract claims -> generate questions."""
    
    print("=" * 80)
    print("GATER WORKFLOW TEST")
    print("=" * 80)
    
    # Step 1: Initialize Gater with URL
    print("\n[1/4] Initializing Gater with URL...")
    gater = Gater(principles_source=TEST_URL)
    # print(f"✓ Gater initialized")
    # print(f"  Text loaded: {len(gater.text)} characters")
    # print(f"  First 200 chars: {gater.text[:200]}...")
    
    # Step 2: Extract claims
    print("\n[2/4] Extracting claims from text...")
    await gater.extract_claims()
    print(f"✓ Claims extracted: {len(gater.claims)} claims found")
    print("\nClaims:")
    for i, claim in enumerate(gater.claims, 1):
        print(f"  {i}. {claim}")
    
    # Step 3: Generate questions
    print("\n[3/4] Generating questions from claims...")
    questions = await gater.generate_questions()
    
    if questions:
        print(f"✓ Questions generated: {len(questions)} questions")
        print("\nQuestions:")
        for i, question in enumerate(questions, 1):
            print(f"  {i}. {question}")
    else:
        print("✗ No questions generated")
        questions = []
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Source: {TEST_URL}")
    print(f"Text length: {len(gater.text)} characters")
    print(f"Claims extracted: {len(gater.claims)}")
    print(f"Questions generated: {len(questions) if questions else 0}")
    print("\n✓ Full workflow completed successfully!")
    
    return gater, questions


if __name__ == "__main__":
    try:
        gater, questions = asyncio.run(test_full_workflow())
    except Exception as e:
        print(f"\n✗ Workflow failed: {e}")
        import traceback
        traceback.print_exc()
