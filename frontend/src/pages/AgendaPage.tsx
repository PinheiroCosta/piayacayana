import { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Event } from '../types/content';
import { Markdown } from '../components/Markdown';

export function AgendaPage() {
  const [events, setEvents] = useState<Event[]>([]);
  useEffect(() => { api.events().then(setEvents); }, []);
  return <>{events.map((e) => <div className="card" key={`${e.title}-${e.start_date}`}><h3>{e.title}</h3><p>{new Date(e.start_date).toLocaleString()} - {e.location}</p><Markdown content={e.description} /></div>)}</>;
}
