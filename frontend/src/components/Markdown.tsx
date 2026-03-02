import DOMPurify from 'dompurify';
import { marked } from 'marked';

export function Markdown({ content }: { content: string }) {
  const html = DOMPurify.sanitize(marked.parse(content) as string);
  return <div dangerouslySetInnerHTML={{ __html: html }} />;
}
