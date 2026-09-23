export const formatDate = (dateString: string): string => {
    const date = new Date(dateString);

    if (isNaN(date.getTime())) return dateString;

    const formattedDate = date.toLocaleDateString('en-GB', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        
    }).replace(/\//g, '.');

    const formattedTime = date.toLocaleTimeString('en-GB', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false,
    });

    return `${formattedDate} : ${formattedTime}`;
}