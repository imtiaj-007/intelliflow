from typing import List


class PromptManager:
    """
    A manager class for handling and generating prompt templates for various AI tasks.

    This class provides methods to generate structured prompts following best practices
    for AI model interactions, particularly for RAG (Retrieval Augmented Generation) systems.
    """

    def estimate_tokens(self, prompt: str) -> int:
        """
        Rough token estimation for context window management.
        ~1 token = 4 characters for English text.
        """
        return len(prompt) // 4

    @property
    def markdown_guidelines(self) -> str:
        return """
Markdown Style Rules (GitHub Style Rendering):
- Use proper headings (#, ##, ###)
- Use bullet points: `-` for main bullets, `*` for grouped content
- Use numbered lists only when order matters
- Use fenced code blocks with language like:
```js
console.log("Hello");
```
- Bold for emphasis (**example**) & *italics* only when needed
- Use tables for structured comparisons
- Keep responses clean, readable & well‑spaced
"""

    def enforce_markdown(self, content: str) -> str:
        return f"""Follow the GitHub‑style Markdown formatting rules below:
{self.markdown_guidelines}
---
Render the following content using those rules:

{content}
"""

    def get_rag_prompt(self, context: str, question: str) -> str:
        """
        Generate a RAG (Retrieval Augmented Generation) prompt template.

        This method constructs a structured prompt that includes context, conversation history,
        and a question to guide the AI model in providing contextually relevant responses.

        Args:
            context (str): The retrieved context/documentation to use for answering the question.
            question (str): The user's question to be answered.
            history (str): The conversation history to maintain context and continuity.

        Returns:
            str: A formatted prompt string ready for use with AI models.

        Example:
            >>> pm = PromptManager()
            >>> prompt = pm.get_rag_prompt("Context text", "What is AI?", "Previous conversation")
        """
        base = f"""You are a helpful AI pdf chatbot assistant. Use the provided context to answer questions accurately.

CONTEXT:
{context}

USER QUESTION:
{question}

INSTRUCTIONS:
1. Answer based PRIMARILY on the provided context
2. If context is insufficient, clearly state what's missing
3. You may supplement with general knowledge, but clearly distinguish between:
   - Information from the context (cite as "According to the documents...")
   - General knowledge (cite as "Based on general knowledge...")
4. Maintain conversation continuity
5. Be precise and helpful

ANSWER:"""

        return self.enforce_markdown(base)

    def get_summarization_prompt(self, text: str, target_length: str = "20-30%") -> str:
        """
        Generate a prompt template for document summarization tasks.

        This method constructs a structured prompt for summarizing text content,
        providing clear instructions for concise and comprehensive summarization.

        Args:
            text (str): The text content to be summarized.

        Returns:
            str: A formatted prompt string for summarization tasks.

        Example:
            >>> pm = PromptManager()
            >>> prompt = pm.get_summarization_prompt("Long document text...")
        """
        base = f"""You are an expert summarization assistant. Please provide a comprehensive yet concise summary of the following text.

INSTRUCTIONS:
1. Capture the main ideas and key points
2. Maintain the original meaning and context
3. Be objective and factual
4. Keep the summary clear and well-structured

TEXT TO SUMMARIZE:
{text}

Please provide a summary that is approximately {target_length} of the original text length.

SUMMARY:"""

        return self.enforce_markdown(base)

    def get_extraction_prompt(self, text: str, fields: List[str]) -> str:
        """
        Generate a prompt template for information extraction tasks.

        This method constructs a structured prompt for extracting specific information
        from text content, with clear formatting instructions for the output.

        Args:
            text (str): The text content from which to extract information.
            fields (List[str]): List of specific information fields to extract.

        Returns:
            str: A formatted prompt string for information extraction tasks.

        Example:
            >>> pm = PromptManager()
            >>> prompt = pm.get_extraction_prompt("Article text...", ["names", "dates", "locations"])
        """
        base = f"""You are an information extraction specialist. Extract the following specific information from the text below:

FIELDS TO EXTRACT:
{', '.join(fields)}

INSTRUCTIONS:
1. Extract only the requested information
2. Be precise and accurate
3. If information is not found for a field, indicate "Not found"
4. Format the output clearly for each field
5. Provide direct quotes when possible

SOURCE TEXT:
{text}

Please extract the information in the following format:
- Field 1: [extracted value]
- Field 2: [extracted value]
- Field 3: [extracted value or "Not found"]

EXTRACTED INFORMATION:"""

        return self.enforce_markdown(base)
