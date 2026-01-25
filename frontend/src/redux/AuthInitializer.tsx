'use client';

import { useEffect } from 'react';
import { useAppDispatch } from './hooks';
import { checkAuthAsync } from './slices/authSlice';

export default function AuthInitializer({ children }: { children: React.ReactNode }) {
    const dispatch = useAppDispatch();

    useEffect(() => {
        dispatch(checkAuthAsync());
    }, [dispatch]);

    return <>{children}</>;
}
