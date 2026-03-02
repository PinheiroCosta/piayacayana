import DOMPurify from 'dompurify';
import { marked } from 'marked';

interface Props {
  markdown: string;
}

export function Markdown({ markdown }: Props) {
  const html = DOMPurify.sanitize(marked.parse(markdown) as string);
  return <div dangerouslySetInnerHTML={{ __html: html }} />;
}
