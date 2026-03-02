import { useEffect, useState } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import { api } from '../services/api';
import { Article } from '../types/content';
import { Markdown } from '../components/Markdown';

export function PreviewArticlePage() {
  const { slug = '' } = useParams();
  const [search] = useSearchParams();
  const token = search.get('token') || '';
  const [article, setArticle] = useState<Article | null>(null);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    api.previewArticle(slug, token).then(setArticle).catch(() => setError('Preview inválido ou expirado.'));
  }, [slug, token]);

  if (error) return <p>{error}</p>;
  if (!article) return <p>Carregando preview...</p>;
  return <div className="card"><h2>Preview: {article.title}</h2><Markdown content={article.content} /></div>;
}
