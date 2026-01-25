/**
 * Dashboard API Client
 * Handles all dashboard-related API calls
 */

import { API_BASE_URL, handleApiError } from './api';
import {
  DashboardResponse,
  QuarterDetailResponse,
  WeekDetailResponse,
  WorkoutDetailResponse,
  CompleteWorkoutRequest,
  SkipWorkoutRequest,
} from '@/types/dashboard.types';

const getAuthToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('token');
  }
  return null;
};

const headers = {
  'Content-Type': 'application/json',
};

/**
 * Fetch complete dashboard hierarchy
 * GET /dashboard/
 */
export const fetchDashboardHierarchy = async (): Promise<DashboardResponse> => {
  const token = getAuthToken();
  try {
    const response = await fetch(`${API_BASE_URL}/dashboard/`, {
      method: 'GET',
      headers: {
        ...headers,
        ...(token && { Authorization: `Bearer ${token}` }),
      },
    });

    if (!response.ok) {
      throw handleApiError(response);
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
};

/**
 * Fetch quarterly phase detail with nested weeks
 * GET /dashboard/quarter/{quarter_id}
 */
export const fetchQuarterDetail = async (
  quarterId: string
): Promise<QuarterDetailResponse> => {
  const token = getAuthToken();
  try {
    const response = await fetch(`${API_BASE_URL}/dashboard/quarter/${quarterId}`, {
      method: 'GET',
      headers: {
        ...headers,
        ...(token && { Authorization: `Bearer ${token}` }),
      },
    });

    if (!response.ok) {
      throw handleApiError(response);
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
};

/**
 * Fetch weekly plan detail with nested workouts
 * GET /dashboard/week/{week_id}
 */
export const fetchWeekDetail = async (weekId: string): Promise<WeekDetailResponse> => {
  const token = getAuthToken();
  try {
    const response = await fetch(`${API_BASE_URL}/dashboard/week/${weekId}`, {
      method: 'GET',
      headers: {
        ...headers,
        ...(token && { Authorization: `Bearer ${token}` }),
      },
    });

    if (!response.ok) {
      throw handleApiError(response);
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
};

/**
 * Fetch single workout detail
 * GET /dashboard/workout/{workout_id}
 */
export const fetchWorkoutDetail = async (
  workoutId: string
): Promise<WorkoutDetailResponse> => {
  const token = getAuthToken();
  try {
    const response = await fetch(`${API_BASE_URL}/dashboard/workout/${workoutId}`, {
      method: 'GET',
      headers: {
        ...headers,
        ...(token && { Authorization: `Bearer ${token}` }),
      },
    });

    if (!response.ok) {
      throw handleApiError(response);
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
};

/**
 * Fetch all workouts for a week
 * GET /dashboard/week/{week_id}/workouts
 */
export const fetchWeekWorkouts = async (weekId: string) => {
  const token = getAuthToken();
  try {
    const response = await fetch(
      `${API_BASE_URL}/dashboard/week/${weekId}/workouts`,
      {
        method: 'GET',
        headers: {
          ...headers,
          ...(token && { Authorization: `Bearer ${token}` }),
        },
      }
    );

    if (!response.ok) {
      throw handleApiError(response);
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
};

/**
 * Mark workout as completed
 * PATCH /dashboard/workout/{workout_id}/complete
 */
export const completeWorkout = async (
  workoutId: string,
  feedback: CompleteWorkoutRequest
): Promise<WorkoutDetailResponse> => {
  const token = getAuthToken();
  try {
    const response = await fetch(
      `${API_BASE_URL}/dashboard/workout/${workoutId}/complete`,
      {
        method: 'PATCH',
        headers: {
          ...headers,
          ...(token && { Authorization: `Bearer ${token}` }),
        },
        body: JSON.stringify(feedback),
      }
    );

    if (!response.ok) {
      throw handleApiError(response);
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
};

/**
 * Mark workout as skipped
 * PATCH /dashboard/workout/{workout_id}/skip
 */
export const skipWorkout = async (
  workoutId: string,
  skipData: SkipWorkoutRequest
): Promise<WorkoutDetailResponse> => {
  const token = getAuthToken();
  try {
    const response = await fetch(
      `${API_BASE_URL}/dashboard/workout/${workoutId}/skip`,
      {
        method: 'PATCH',
        headers: {
          ...headers,
          ...(token && { Authorization: `Bearer ${token}` }),
        },
        body: JSON.stringify(skipData),
      }
    );

    if (!response.ok) {
      throw handleApiError(response);
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
};
