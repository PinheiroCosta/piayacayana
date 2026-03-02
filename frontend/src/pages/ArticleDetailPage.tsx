import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../services/api';
import { Article } from '../types/content';
import { Markdown } from '../components/Markdown';

export function ArticleDetailPage() {
  const { slug = '' } = useParams();
  const [article, setArticle] = useState<Article | null>(null);
  useEffect(() => { api.article(slug).then(setArticle); }, [slug]);
  if (!article) return <p>Carregando...</p>;
  return <div className="card"><h2>{article.title}</h2>{article.cover_image && <img src={article.cover_image} alt={article.title} />}
    {article.youtube_video_id && <iframe title="youtube" width="560" height="315" src={`https://www.youtube.com/embed/${article.youtube_video_id}`} />}
    <Markdown content={article.content} /></div>;
}
