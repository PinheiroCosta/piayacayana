import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Article } from '../types/content';

export function ArticlesListPage() {
  const [items, setItems] = useState<Article[]>([]);
  useEffect(() => { api.articles().then(setItems); }, []);
  return <>{items.map((a) => <div className="card" key={a.slug}><h3><Link to={`/artigos/${a.slug}`}>{a.title}</Link></h3><p>{a.summary}</p></div>)}</>;
}
