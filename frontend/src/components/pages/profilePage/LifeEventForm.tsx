'use client';

import { useState } from 'react';

export interface LifeEventData {
  event_type: string;
  description: string;
  impact_level: string;
}

interface LifeEventFormProps {
  onSubmit: (event: LifeEventData) => void;
  onCancel: () => void;
}

export default function LifeEventForm({ onSubmit, onCancel }: LifeEventFormProps) {
  const [formData, setFormData] = useState({
    event_type: 'job_change',
    description: '',
    impact_level: 'medium',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-6 z-50">
      <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-8 max-w-md w-full">
        <h2 className="text-2xl font-bold mb-6">Record Life Event</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Event Type */}
          <div>
            <label className="block text-sm font-medium mb-2">Event Type</label>
            <select
              value={formData.event_type}
              onChange={(e) => setFormData({ ...formData, event_type: e.target.value })}
              className="w-full bg-black/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-[var(--primaryColor)]"
            >
              <option value="job_change">Job Change</option>
              <option value="moving">Moving/Relocation</option>
              <option value="relationship">Relationship Change</option>
              <option value="health">Health Issue</option>
              <option value="family">Family Event</option>
            </select>
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium mb-2">Description</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Describe what's happening..."
              className="w-full bg-black/50 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-[var(--primaryColor)] min-h-[100px]"
              required
            />
          </div>

          {/* Impact Level */}
          <div>
            <label className="block text-sm font-medium mb-2">Impact on Routine</label>
            <select
              value={formData.impact_level}
              onChange={(e) => setFormData({ ...formData, impact_level: e.target.value })}
              className="w-full bg-black/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-[var(--primaryColor)]"
            >
              <option value="low">Low - Minor adjustments</option>
              <option value="medium">Medium - Moderate changes</option>
              <option value="high">High - Major disruption</option>
            </select>
          </div>

          {/* Buttons */}
          <div className="flex gap-3 mt-6">
            <button
              type="button"
              onClick={onCancel}
              className="flex-1 bg-white/10 text-white font-bold py-3 rounded-xl hover:bg-white/20 transition-all"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex-1 bg-[var(--primaryColor)] text-black font-bold py-3 rounded-xl hover:scale-105 transition-transform"
            >
              Save Event
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
