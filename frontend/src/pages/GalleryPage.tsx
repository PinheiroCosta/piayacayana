import { useEffect, useState } from 'react';
import { api } from '../services/api';
import { GalleryItem } from '../types/content';

export function GalleryPage() {
  const [items, setItems] = useState<GalleryItem[]>([]);
  useEffect(() => { api.gallery().then(setItems); }, []);
  return <>{items.map((i) => <div className="card" key={`${i.type}-${i.slug}`}><h3>{i.title}</h3>{i.cover_image && <img src={i.cover_image} alt={i.title} />}
  {i.youtube_video_id && <iframe title={i.slug} width="560" height="315" src={`https://www.youtube.com/embed/${i.youtube_video_id}`} />}</div>)}</>;
}
