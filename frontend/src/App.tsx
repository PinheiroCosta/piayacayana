import { Link, Route, Routes, useParams, useSearchParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { apiClient } from './api/apiClient';
import { ArticleDTO, EventDTO, GalleryItemDTO } from './api/types';
import { Markdown } from './components/Markdown';

function Home() { return <main><h1>Coletivo Piaya Cayana</h1></main>; }
function Sobre() { return <main><h1>Sobre</h1></main>; }
function Contato() { return <main><h1>Contato</h1></main>; }

function Artigos() {
  const [items, setItems] = useState<ArticleDTO[]>([]);
  useEffect(() => { apiClient.getArticles().then(setItems); }, []);
  return <main><h1>Artigos</h1>{items.map((a) => <div className="card" key={a.slug}><Link to={`/artigos/${a.slug}`}>{a.title}</Link></div>)}</main>;
}

function ArtigoDetalhe() {
  const { slug = '' } = useParams();
  const [item, setItem] = useState<ArticleDTO | null>(null);
  useEffect(() => { apiClient.getArticle(slug).then(setItem); }, [slug]);
  if (!item) return <main>Carregando...</main>;
  return <main><h1>{item.title}</h1><Markdown markdown={item.content} /></main>;
}

function Agenda() {
  const [events, setEvents] = useState<EventDTO[]>([]);
  useEffect(() => { apiClient.getEvents().then(setEvents); }, []);
  return <main><h1>Agenda</h1>{events.map((e) => <div className="card" key={e.title}>{e.title}</div>)}</main>;
}

function Galeria() {
  const [items, setItems] = useState<GalleryItemDTO[]>([]);
  useEffect(() => { apiClient.getGallery().then(setItems); }, []);
  return <main><h1>Galeria</h1>{items.map((g) => <div className="card" key={`${g.type}-${g.title}`}><h3>{g.title}</h3>{g.youtube_video_id && <iframe src={`https://www.youtube.com/embed/${g.youtube_video_id}`} title={g.title} />}</div>)}</main>;
}

function PreviewArtigo() {
  const { slug = '' } = useParams();
  const [search] = useSearchParams();
  const token = search.get('token') ?? '';
  const [item, setItem] = useState<ArticleDTO | null>(null);
  useEffect(() => { apiClient.getPreviewArticle(slug, token).then(setItem); }, [slug, token]);
  if (!item) return <main>Carregando preview...</main>;
  return <main><h1>Preview: {item.title}</h1><Markdown markdown={item.content} /></main>;
}

export function App() {
  return (
    <>
      <nav>
        <Link to="/">Início</Link><Link to="/agenda">Agenda</Link><Link to="/galeria">Galeria</Link><Link to="/artigos">Artigos</Link><Link to="/sobre">Sobre</Link><Link to="/contato">Contato</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/agenda" element={<Agenda />} />
        <Route path="/galeria" element={<Galeria />} />
        <Route path="/artigos" element={<Artigos />} />
        <Route path="/artigos/:slug" element={<ArtigoDetalhe />} />
        <Route path="/sobre" element={<Sobre />} />
        <Route path="/contato" element={<Contato />} />
        <Route path="/preview/artigos/:slug" element={<PreviewArtigo />} />
      </Routes>
    </>
  );
}
