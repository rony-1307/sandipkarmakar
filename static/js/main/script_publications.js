function showButtonState(button, message, originalText) {
  button.textContent = message;
  setTimeout(() => {
    button.textContent = originalText;
  }, 1200);
}

function fallbackCopyText(text, button) {
  const originalText = button.textContent;
  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.setAttribute('readonly', '');
  textarea.style.position = 'fixed';
  textarea.style.opacity = '0';
  document.body.appendChild(textarea);
  textarea.select();
  textarea.setSelectionRange(0, textarea.value.length);

  try {
    document.execCommand('copy');
    showButtonState(button, 'Copied', originalText);
  } catch (error) {
    showButtonState(button, 'Copy failed', originalText);
  } finally {
    document.body.removeChild(textarea);
  }
}

function copyCitation(button) {
  const citation = button.dataset.citation || button.getAttribute('data-citation') || '';
  const originalText = button.textContent;
  if (!citation) {
    showButtonState(button, 'No citation', originalText);
    return;
  }

  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(citation)
      .then(() => showButtonState(button, 'Copied', originalText))
      .catch(() => fallbackCopyText(citation, button));
  } else {
    fallbackCopyText(citation, button);
  }
}