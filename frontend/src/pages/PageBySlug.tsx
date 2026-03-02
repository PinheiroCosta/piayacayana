import { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Page } from '../types/content';
import { Markdown } from '../components/Markdown';

export function PageBySlug({ slug }: { slug: string }) {
  const [page, setPage] = useState<Page | null>(null);

  useEffect(() => { api.page(slug).then(setPage).catch(() => setPage(null)); }, [slug]);
  if (!page) return <p>Conteúdo indisponível.</p>;
  return <div className="card"><h2>{page.title}</h2><Markdown content={page.content} /></div>;
}
